import pytest
import os
from os.path import join, exists
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from syncloudlib.integration.installer import get_data_dir, get_app_dir, get_service_prefix, get_ssh_env_vars, get_snap_data_dir
from syncloudlib.integration.device import Device
from syncloudlib.integration.selenium_wrapper import SeleniumWrapper

SYNCLOUD_INFO = 'syncloud.info'


def pytest_addoption(parser):
    parser.addoption("--domain", action="store")
    parser.addoption("--device-host", action="store")
    parser.addoption("--app-archive-path", action="store")
    parser.addoption("--app", action="store")
    parser.addoption("--ui-mode", action="store", default="desktop")
    parser.addoption("--device-user", action="store", default="user")
    parser.addoption("--build-number", action="store", default="local")


@pytest.fixture(scope='session')
def build_number(request):
    return request.config.getoption("--build-number")
    

@pytest.fixture(scope='session')
def device_user(request):
    return request.config.getoption("--device-user")
    
    
@pytest.fixture(scope='session')
def device_password():
    return 'Password1'
    

@pytest.fixture(scope='session')
def redirect_user():
    return "teamcity@syncloud.it"


@pytest.fixture(scope='session')
def redirect_password():
    return "password"
    
    
@pytest.fixture(scope='session')
def app(request):
    return request.config.getoption("--app")


@pytest.fixture(scope='session')
def ui_mode(request):
    return request.config.getoption("--ui-mode")


@pytest.fixture(scope='session')
def app_archive_path(request):
    return request.config.getoption("--app-archive-path")


@pytest.fixture(scope='session')
def device_host(request):
    return request.config.getoption("--device-host")


@pytest.fixture(scope='session')
def domain(request):
    return request.config.getoption("--domain")


@pytest.fixture(scope='session')
def main_domain():
    return SYNCLOUD_INFO


@pytest.fixture(scope='session')
def device_domain(domain, main_domain):
    return '{0}.{1}'.format(domain, main_domain)


@pytest.fixture(scope='session')
def app_domain(app, device_domain):
    return '{0}.{1}'.format(app, device_domain)
    

@pytest.fixture(scope="session")
def platform_data_dir():
    return get_data_dir('platform')

    
@pytest.fixture(scope="session")
def data_dir(app):
    return get_data_dir(app)


@pytest.fixture(scope="session")
def snap_data_dir(app):
    return get_snap_data_dir(app)


@pytest.fixture(scope="session")
def app_dir(app):
    return get_app_dir(app)
    

@pytest.fixture(scope="session")
def service_prefix():
    return get_service_prefix()


def new_profile(user_agent):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('app.update.auto', False)
    profile.set_preference('app.update.enabled', False)
    profile.set_preference("general.useragent.override", user_agent)
    profile.set_preference("devtools.console.stdout.content", True)

    return profile


def new_driver(profile):

    caps = DesiredCapabilities.FIREFOX
    caps['acceptSslCerts'] = True
    caps['acceptInsecureCerts'] = True
    caps['javascriptEnabled'] = True

    return webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        desired_capabilities=caps,
        browser_profile=profile
    )


@pytest.fixture(scope="module")
def desktop_driver(log_dir, ui_mode):
    profile = new_profile("Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0")
    driver = new_driver(profile)
    driver.set_window_position(0, 0)
    driver.set_window_size(1024, 2000)
    return driver
    
    
@pytest.fixture(scope="module")
def mobile_driver(log_dir, ui_mode):    
    profile = new_profile(
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) "
        "AppleWebKit/528.18 (KHTML, like Gecko) "
        "Version/4.0 Mobile/7A341 Safari/528.16")
    driver = new_driver(profile)
    driver.set_window_position(0, 0)
    driver.set_window_size(400, 2000)
    return driver


@pytest.fixture(scope="module")
def driver(mobile_driver, desktop_driver, ui_mode):    
    if ui_mode == "desktop":
        return desktop_driver
    else:
        return mobile_driver


@pytest.fixture(scope="session")
def ssh_env_vars(app):
    return get_ssh_env_vars(app)


@pytest.fixture(scope='function')
def device_session(device):
    return device.login()


@pytest.fixture(scope="session")
def device(main_domain, device_host, domain, device_user,
           device_password, redirect_user, redirect_password, ssh_env_vars):

    return Device(main_domain, device_host, domain, device_user,
                  device_password, redirect_user, redirect_password, ssh_env_vars)


@pytest.fixture(scope="session")
def log_dir(project_dir):
    dir = join(project_dir, 'log')
    if not exists(dir):
        os.mkdir(dir)
    return dir


@pytest.fixture(scope="session")
def artifact_dir(project_dir):
    dir = join(project_dir, 'artifact')
    if not exists(dir):
        os.mkdir(dir)
    return dir


@pytest.fixture(scope="session")
def screenshot_dir(artifact_dir):
    dir = join(artifact_dir, 'screenshot')
    if not exists(dir):
        os.mkdir(dir)
    return dir


@pytest.fixture(scope="module")
def selenium(driver, ui_mode, screenshot_dir, app_domain):
    return SeleniumWrapper(driver, ui_mode, screenshot_dir, app_domain)
