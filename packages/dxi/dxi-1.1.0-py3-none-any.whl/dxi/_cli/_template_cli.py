#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click
from dxi._lib.util import boolean_based_system_exit
from dxi.template.dxi_template import DXITemplate
from dxi.template.dxi_template import DXITemplateConstants


@click.group()
def template():
    """
    Command for all Self Service Template related operations
    """
    pass


# List Command
@template.command()
@click.option("--engine", default=DXITemplateConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXITemplateConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXITemplateConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXITemplateConstants.POLL,
)
def list(engine, single_thread, config, log_file_path, poll):
    """
    List all Self Service Templates on a given engine
    """
    temp_obj = DXITemplate(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(temp_obj.list())


# Create Template Command
@click.option(
    "--templatename", required=True, help=" Name of the template to create"
)
@click.option(
    "--dbnames",
    required=True,
    help="List of data sources to add to the new template"
    "If the template should contain multiple data source, "
    "separate the names with colon (:). "
    "Sample: db1:db2:db3",
)
@click.option("--engine", default=DXITemplateConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXITemplateConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXITemplateConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXITemplateConstants.POLL,
)
@template.command()
def create(
    templatename, dbnames, engine, single_thread, config, log_file_path, poll
):
    """
    Create the Self Service Template
    dxi template create --templatename template --dbnames vOraCRM_BRKFIX
    """
    temp_obj = DXITemplate(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        temp_obj.create(template_name=templatename, dbnames=dbnames)
    )


# Delete Template Command
@click.option("--templatename", required=True, help="Name of the SS Container")
@click.option("--engine", default=DXITemplateConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXITemplateConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXITemplateConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXITemplateConstants.POLL,
)
@template.command()
def delete(templatename, engine, single_thread, config, log_file_path, poll):
    """
    Deletes a Template
    dxi template delete --templatename t1
    """
    ss_container = DXITemplate(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(ss_container.delete(template_name=templatename))


if __name__ == "__main__":
    delete()
