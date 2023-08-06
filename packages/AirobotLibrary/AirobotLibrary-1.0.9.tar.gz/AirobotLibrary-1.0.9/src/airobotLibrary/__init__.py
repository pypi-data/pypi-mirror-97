from .air_selenium import AirSelenium
from DatabaseLibrary import DatabaseLibrary as AirDatabase
from AppiumLibrary import AppiumLibrary as AirAppium
from DiffLibrary import DiffLibrary as AirDiff
from RequestsLibrary import RequestsLibrary as AirRequests
from ArchiveLibrary import ArchiveLibrary as AirArchive
from FtpLibrary import FtpLibrary as AirFtp
from airtest.core.settings import Settings as ST


ST.REMOTE_URL = None
ST.BROWSER = 'Chrome'
