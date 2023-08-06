"""
Documentation
-------------
XmindToTestlink is a tool to help you convert xmindzen file to testlink recognized xml files,
then you can import it into testlink as test suite , test cases and requirement.

For more detail, please go to: https://github.com/DancePerth/XmindToTestlink

"""

from setuptools import setup, find_packages

long_description = __doc__

def main():
    setup(
        name="XmindToTestlink",
        description="Convert xmindzen to TestLink xml",
        keywords="xmind testlink import converter testing testcase requirement",
        long_description=long_description,
        version="1.6.0",
        author="DancePerth",
        author_email="28daysinperth@gmail.com",
        url="https://github.com/DancePerth/XmindToTestlink",
        packages=find_packages(),
        package_data={},
        entry_points={
            'console_scripts':[
                'xmindtotestlink=XmindToTestlink.main:main',
                'rexmind=XmindToTestlink.rexmind:md_to_xmind',
                'cchip=XmindToTestlink.check_xmind:check_xmind',
                'xmlupdate=XmindToTestlink.xml_update:main',
                'xmind2obs=XmindToTestlink.xmind_to_obsidian:main'
                ]
            }
    )


if __name__ == "__main__":
    main()
