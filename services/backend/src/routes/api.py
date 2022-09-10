#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#   src/routes/api.py
#

from fastapi import APIRouter
from src.routes import users, notes, roles

api_router = APIRouter()

api_router.include_router(users.router, tags=['Users'])
api_router.include_router(roles.router, tags=['User roles'])
api_router.include_router(notes.router, tags=['Notes'])

# example of openshift health router
#api_router.include_router(
#    health.router,
#    prefix="/health",
#    tags=["Health check"]
#)
