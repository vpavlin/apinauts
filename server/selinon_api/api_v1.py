#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################

import logging
from .connection import Connection
from .connection import requires_initialized_selinon
from selinon import StoragePool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@requires_initialized_selinon
def post_run_flow(flow_name, node_args=None):
    """ Handler called on POST on /api/v1/run-flow

    :param flow_name: name of flow to be run
    :param node_args: arguments supplied to flow
    :return: resulting dict for the request
    """
    logger.info("Scheduling flow '%s' with node_args: '%s'", flow_name, node_args)
    dispatcher = Connection.run_selinon_flow(flow_name, node_args)
    return {"dispatcher_id": dispatcher.id, "flow_name": flow_name}, 201


@requires_initialized_selinon
def post_transactions(title, category, currency, second_party, amount):
    logger.info("Saving transaction %s", title)
    db = StoragePool.get_connected_storage("PostgreSQL")
    transaction_id = db.create_transaction(title, category, currency, second_party, amount)
    return {"transaction_id": transaction_id}

@requires_initialized_selinon
def post_categories(name, hidden=False):
    logger.info("Saving category %s", name)
    db = StoragePool.get_connected_storage("PostgreSQL")
    category_name = db.create_category(name, hidden)
    return {"category_name": category_name}

@requires_initialized_selinon
def get_categories():
    logger.info("Getting categories")
    db = StoragePool.get_connected_storage("PostgreSQL")
    categories = db.get_categories()
    return categories

@requires_initialized_selinon
def get_transactions_per_category(category):
    logger.info("Getting transactions for category %s", category)
    db = StoragePool.get_connected_storage("PostgreSQL")
    transactions = db.get_transactions_per_category(category)
    return transactions

@requires_initialized_selinon
def get_transactions():
    logger.info("Getting transactions")
    db = StoragePool.get_connected_storage("PostgreSQL")
    transactions = db.get_transactions()
    return transactions

@requires_initialized_selinon
def post_budgets(category, month, year, amount):
    logger.info("Saving budget for category %s", category)
    db = StoragePool.get_connected_storage("PostgreSQL")
    budget_id = db.create_budgets(category, month, year, amount)
    return {"budget_id": budget_id}

@requires_initialized_selinon
def get_budgets():
    logger.info("Getting budgets")
    db = StoragePool.get_connected_storage("PostgreSQL")
    budgets = db.get_budgets()
    return budgets