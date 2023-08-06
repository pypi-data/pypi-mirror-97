# DEVELOP
Doc for developers

Clone code to local

```bash
git clone --depth 5 https://github.com/alibaba/tidevice
```

## View DeveloperDiskImage Content
For example

```bash
hdiutil mount /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/DeviceSupport/14.0/DeveloperDiskImage.dmg
tree /Volumes/DeveloperDiskImage
```

## How to Package WDA.ipa
Build `WebDriverAgentRunnerUITests-Runner.app` with the following command. `.app` should located in `/tmp/derivedDataPath/Release-iphoneos`

```bash
xcodebuild build-for-testing -workspace WebDriverAgent.xcworkspace/ -scheme WebDriverAgent -sdk iphoneos -configuration Release -derivedDataPath /tmp/derivedDataPath
```

Created folder `Payload` and put `.app` into it, then compressed to zip, change extention name to `.ipa`, and resign. That's all.


## Publish package to Pypi using Github Actions
Ref: https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/


## References
- C implementation <https://github.com/libimobiledevice>
- Python implement of libimobiledevice: <https://github.com/iOSForensics/pymobiledevice>
- Apple Device Images: <https://github.com/iGhibli/iOS-DeviceSupport>
- <https://github.com/troybowman/dtxmsg>
- <https://github.com/troybowman/ios_instruments_client>
- Binary of libimobiledevice for Windows <http://docs.quamotion.mobi/docs/imobiledevice/>
- https://pypi.org/project/hexdump/