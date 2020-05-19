mycloudhome --debug login --username xxx --password xxx
mycloudhome --debug devices
mycloudhome --debug ls --wduri 'wd://Buckets/install/v2ray-linux-arm64.zip'
mycloudhome --debug mv --src wd://temp/readme.md --dst wd://temp/ttt
mycloudhome --debug rename --wduri wd://temp/readme_1.md --name 2.md
mycloudhome --debug rm --wduri wd://temp/readme_1.md
mycloudhome --debug download --wduri 'wd://Buckets/install/v2ray-linux-arm64.zip' .
mycloudhome --debug upload --src 20200518_CDF.xlsx --wduri wd://temp