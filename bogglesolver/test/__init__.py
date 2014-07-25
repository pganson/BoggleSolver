#!/usr/bin/env python

"""Tests for the bogglesolver package."""

import unittest
from unittest.mock import patch, Mock, MagicMock

import os


ENV = 'TEST_INTEGRATION'  # environment variable to enable integration tests
REASON = "'{0}' variable not set".format(ENV)
