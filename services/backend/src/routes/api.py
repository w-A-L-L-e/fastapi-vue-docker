#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#   src/routes/api.py
#

from src.routes import users, notes, roles
from fastapi import APIRouter
from tortoise import Tortoise

# we need to init models before
# importing routes so that nested relations work
# https://tortoise-orm.readthedocs.io/en/latest/contrib/pydantic.html#relations-early-init
Tortoise.init_models(["src.database.models"], "models")


api_router = APIRouter()
api_router.include_router(users.router, tags=['Users'])
api_router.include_router(roles.router, tags=['User roles'])
api_router.include_router(notes.router, tags=['Notes'])

# example of openshift health router
# api_router.include_router(
#    health.router,
#    prefix="/health",
#    tags=["Health check"]
# )
