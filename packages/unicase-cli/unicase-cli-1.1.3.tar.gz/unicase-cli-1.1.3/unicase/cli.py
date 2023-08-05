#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : mocobk
# @Email : mailmzb@qq.com
# @Time : 2021/2/21 18:15
import time
from pathlib import Path

import click
from terminal_layout import Fore
from terminal_layout.extensions.choice import Choice, StringStyle

from unicase import utils
from unicase.utils import BVTCases, Cases

CONFIG = utils.Config()
CONFIG_DATA = CONFIG.get() or {}
CONFIG_DATA.setdefault('base_url', utils.TAPD_BASE_URL)


# TODO: 加入 verbose 日志
@click.group()
def cli():
    """UNI 测试用例管理工具"""


@cli.command()
@click.option('--tester', required=False, help='当前测试人员英文名')
@click.option('--base-url', required=False, help='当前 API Base Url')
def config(tester, base_url):
    """配置测试人员、API Base Url"""
    if tester:
        CONFIG_DATA['tester'] = tester
        click.echo(click.style(f'当前配置的测试人员：{tester}', fg='bright_cyan', bold=True))
    if base_url:
        CONFIG_DATA['base_url'] = base_url
        click.echo(click.style(f'当前配置的 Base Url：{base_url}', fg='bright_cyan', bold=True))
    if tester or base_url:
        CONFIG.put(CONFIG_DATA)
    else:
        click.echo(click.style(f'tester={CONFIG_DATA.get("tester") or "未配置"}', fg='bright_cyan', bold=True))
        click.echo(click.style(f'base_url={CONFIG_DATA.get("base_url")}', fg='bright_cyan', bold=True))
        click.echo(
            click.style(f'请输入 unicase --tester <name> 或 unicase --base-url <base url> 进行配置', fg='bright_cyan',
                        bold=True))


def check_config(ctx):
    if CONFIG_DATA.get('tester') is None:
        click.echo(click.style('请先配置测试人员英文名', fg='bright_cyan', bold=True))
        ctx.invoke(config)
        ctx.exit()


@cli.command()
@click.option('--name', required=False, help='指定生成的文件路径，默认生成到当前文件夹且以迭代名称命名')
@click.pass_context
def create(ctx, name):
    """创建 Excel 用例模板文件"""
    check_config(ctx)

    tapd = utils.Tapd(CONFIG_DATA.get('base_url'))
    iterations = tapd.get_tapd_iterations()

    select = Choice('请选择用例所属的迭代: (按 <esc> 退出) ',
                    list(iterations.keys()),
                    icon_style=StringStyle(fore=Fore.lightcyan),
                    selected_style=StringStyle(fore=Fore.lightcyan))

    choice = select.get_choice()
    if choice:
        index, iteration_name = choice
        target_file_path = Path(name) if name else Path('./').joinpath(
            f'{utils.secure_filename(iteration_name)}({CONFIG_DATA.get("tester")}).xlsm'
        )
        iteration_id = iterations[iteration_name]
        tapd.set_iteration_id(iteration_id)

        excel = utils.Excel(utils.TEMPLATE_XLS, tapd)
        excel.set_sheet_name(iteration_name)

        # 将迭代信息存储在用例表的A1单元格，方便后面上传用例使用
        excel.set_iteration_meta_info({
            'iteration_id': iteration_id,
            'iteration_name': iteration_name,
            'iteration_stories': tapd.get_tapd_iteration_stories()
        })
        excel.set_iteration_data_validation()
        excel.save(target_file_path)
        click.echo(click.style(str(target_file_path.absolute()), fg='green', bold=True))


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--type', default='bvt', type=click.Choice(['bvt', 'all'], case_sensitive=False),
              help='用例上传类型：bvt 冒烟用例，all 全部用例')
@click.pass_context
def upload(ctx, file, type: str):
    """上传 Excel 用例到 TAPD"""
    check_config(ctx)

    tapd = utils.Tapd(CONFIG_DATA.get('base_url'))
    excel = utils.Excel(file, tapd)
    iteration_meta_info = excel.get_iteration_meta_info()

    iteration_id = iteration_meta_info['iteration_id']
    iteration_name = iteration_meta_info['iteration_name']

    tapd.set_iteration_id(iteration_id)

    if not iteration_meta_info:
        click.echo(click.style('用例元信息丢失，请补充后再上传', fg='bright_red', bold=True))
        ctx.exit()
    click.echo(click.style(f'迭代: {iteration_name}', fg='bright_red', bold=True))
    if type.lower() == 'bvt':
        case_type = '冒烟'
        cases = BVTCases(excel)
    else:
        case_type = '所有'
        cases = Cases(excel)

    results, cases_count = cases.validate_data()
    if results:
        for reason in results:
            click.echo(click.style(reason, fg='bright_red', bold=True))
        ctx.exit()
    else:
        if click.confirm(click.style(f'即将上传或更新{case_type}用例数 {cases_count} 条， 是否继续？', fg='bright_cyan', bold=True)):
            cases.upload(CONFIG_DATA.get('tester'))
            click.echo(click.style('上传成功', fg='bright_cyan', bold=True))

            # 因为重新编辑后的 Excel 会丢失数据校验数据，这里上传完后重新加入数据校验
            # openpyxl/worksheet/_reader.py:308:
            # UserWarning: Data Validation extension is not supported and will be removed
            excel.set_iteration_meta_info({
                'iteration_id': iteration_meta_info['iteration_id'],
                'iteration_name': iteration_meta_info['iteration_name'],
                'iteration_stories': tapd.get_tapd_iteration_stories()
            })
            excel.set_iteration_data_validation()
            file_name = file
            try:
                excel.save(filename=file_name)
            # 同名保存失败大部分是因为用例文件是打开状态，无权限写入，重新取名保存
            except Exception:
                file_name = time.strftime('%Y%m%d%H%M%S') + file
                excel.save(filename=file_name)

            click.echo(click.style('用例文件已更新', fg='green', bold=True))
            click.echo(click.style(str(Path(file_name).absolute()), fg='green', bold=True))
