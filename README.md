# Fortune Lyric - 随机洛天依歌曲歌词

此项目提供了一个洛天依的经典曲目歌词选段的数据库，并以此实现了一个获得随机歌词的程序。

灵感来源：[一言](https://hitokoto.cn/)、[Fortune](https://en.wikipedia.org/wiki/Fortune_(Unix))。

## 使用方法

支持的使用方法包括：
 - 在任何支持 bash 的系统（Windows 需要额外安装 bash，Linux / MacOS 一般不需要）中，通过调用命令来获得随机歌词，也可以配置为每次登陆 SSH 时显示。
 - 通过网页 API 获得随机歌词。
 - 在自己的项目、程序中，嵌入数据库文本文件或 JSON 文件，并进行调用。

### 在 bash 中使用

**抽取结果为单行的版本：**

```bash
curl -L https://github.com/luotianyi-dev/fortune-lyric/releases/latest/download/fortune-lyric.bash -o /usr/local/bin/fortune-lyric && chmod +x /usr/local/bin/fortune-lyric
```

中国大陆镜像：
```bash
curl -L https://lty.vc/lotd/bash -o /usr/local/bin/fortune-lyric && chmod +x /usr/local/bin/fortune-lyric
```

显示效果如：
```
思念的含义在无尽生命中淡去 帷幕落下喝彩响起 片刻后都沉寂
```

**抽取结果为多行的版本：**

```bash
curl -L https://github.com/luotianyi-dev/fortune-lyric/releases/latest/download/fortune-lyric-banner.bash -o /usr/local/bin/fortune-lyric && chmod +x /usr/local/bin/fortune-lyric
```

中国大陆镜像：
```bash
curl -L https://lty.vc/lotd/banner-bash -o /usr/local/bin/fortune-lyric && chmod +x /usr/local/bin/fortune-lyric
```

显示效果如：
```
$ fortune-lyric
思念的含义在无尽生命中淡去
帷幕落下喝彩响起 片刻后都沉寂

                -- COP 《为了你唱下去》, 2016
```

### 配置为 SSH Banner
**Ubuntu / Debian**
将上面的命令替换为：
```bash
curl -L <安装地址> -o /etc/update-motd.d/25-fortune-lyric && chmod +x /etc/update-motd.d/25-fortune-lyric
```

**Arch Linux**
```bash
pacman -S run-parts bash curl
mkdir -p /etc/update-motd.d
echo 'session    optional    pam_exec.so    stdout /usr/bin/run-parts /etc/update-motd.d' >> /etc/pam.d/system-login
curl -L <安装地址> -o /etc/update-motd.d/25-fortune-lyric && chmod +x /etc/update-motd.d/25-fortune-lyric
```

### 通过网页调用
直接打开 https://lty.vc/lotd 即可获得随机歌词。

```
curl -L lty.vc/lotd

思念的含义在无尽生命中淡去
帷幕落下喝彩响起 片刻后都沉寂
```

### 下载数据库
请在 GitHub Release 页面下载数据库文件。


| Release File                  | Description            |
| ----------------------------- | ---------------------- |
| `fortune-lyric.json`          | JSON 格式              |
| `fortune-lyric-minified.json` | JSON 格式（最小化）    |
| `fortune-lyric.txt`           | 单行文本格式           |
| `fortune-lyric-source.txt`    | 人类可读 (源代码) 格式 |


如果 GitHub 下载过慢，也可以使用我们的镜像：

| URL                               | Description            |
| --------------------------------- | ---------------------- |
| https://lty.vc/lotd/json          | JSON 格式              |
| https://lty.vc/lotd/minified-json | JSON 格式（最小化）    |
| https://lty.vc/lotd/txt           | 单行文本格式           |
| https://lty.vc/lotd/source-txt    | 人类可读 (源代码) 格式 |


## 版权

**请注意：此项目不是开源软件。** 此项目的分发、使用、修改、衍生等相关规定均比开源项目更为严格。

 1. 代码部分。代码部分指的是除了本项目的 `database.txt` 以外，所有在本项目 Git 仓库中的代码。此项目的代码部分由 ChatGPT 所编写。目前 AI 编写的代码版权所属在法律界尚不明确，用户应自行承担相关风险。此项目的贡献者放弃未来一切可能的对此项目代码部分的版权主张。
 2. 数据库部分。数据库指的是本项目中 `database.txt` 的部分。此项目的数据库部分为歌词，其著作权属于原著作权人。您在使用过程中，应遵守中文虚拟歌手社区的相关规定，包括但不限于[《Vsinger同人创作规约》](https://vsinger.com/aboutus#%E7%89%88%E6%9D%83%E8%AF%B4%E6%98%8E)。此外，您还需要遵守歌曲原作者的二次创作规定。您对此项目的任何分发、使用、修改、衍生等行为，均应确保符合歌词原作者的相关规定或获得授权。此项目的贡献者基于对相关数据的收集、整理、组织的贡献，要求您在使用此项目数据库部分及其产物时，遵守更加严格的限制。
 3. API 调用。若你使用 API 调用方式使用本项目，即代表您同意 lty.vc 的服务政策和隐私条款。lty.vc 有权收集您调用 API 的服务器信息、软件信息和网络信息，若通过前端 CROS 方式调用，lty.vc 亦会收集您的用户的设备信息、浏览器信息和网络信息。您应将 lty.vc 的隐私政策及所收集的信息告知您的用户。以商业为目的的网站、App、软件，包括但不限于要求用户付费以解锁内容、通过网站销售实体或虚拟产品的网站，不得使用本项目的 API 服务。lty.vc 有权对调用 API 的网站、App、软件进行评估，若相关网站、App、软件含有违反法律法规规定的内容，或含有对虚拟歌手及虚拟歌手创作者攻击、侮辱、抹黑内容的，lty.vc 有权终止其服务。通过 API 调用的，应在网站底部或友情链接页面，标明使用了由「传输控制协议TCP」开发的 lty.vc API 服务，并标明「传输控制协议TCP」的哔哩哔哩账号地址 https://space.bilibili.com/1425000748 和 lty.vc 的 API 地址 https://docs.lty.vc/ 。
 4. 产物分发。产物指的是本项目的编译结果，即将本项目的数据库部分输入本项目的代码部分，经过代码部分处理得到的文件。使用 GitHub Release 及 lty.vc 分发的产物，为官方产物。用户使用此项目的 Git 仓库，运行代码部分得到的文件，为非官方产物。由于产物内包括数据库部分的内容，故分发、使用、修改产物或将产物嵌入您的产品，亦需遵守中文虚拟歌手社区的相关规定及歌曲原作者的二次创作规定，或获得相关授权。在分发产物时，应向用户提供此项目的许可证，即本文档「版权」一节 1 至 10 条的全部内容。
 5. 非商业使用。您不得以商业目的使用此项目。您不得将此项目的数据库部分或产物嵌入任何商用产品或服务。以企业、事业单位、非盈利组织、社会团体及任何法人性质的组织为主体开办的服务或生产的产品，不得嵌入此项目的数据库部分或产物。您不得在雇主、学校、研究所等您所在单位的计算机上使用此项目的产物，除非您的所在单位为以中文虚拟歌手创作为主要业务。
 6. 与您的产品隔离。若您在您的项目、产品或服务中使用、分发或嵌入此项目的数据库部分或产物，无论您的项目、产品或服务是否开发源代码、是否为商业性质，您都应采取措施将此项目的数据库部分或产物与您的项目、产品或服务隔离。对未形成有效隔离的项目，您的项目、产品或服务的版权声明及主张，对使用、分发或嵌入此项目数据库或产物的部分无效。您不得对本项目及其产物进行再许可。
 7. 修改与衍生。您可以随意修改与衍生此项目的代码部分。您可以修改此项目的数据库及其产物，但不得向任何第三人分发修改后的内容及其产物，除非您以相同的许可证、以相对便利可获取的方式、不设门槛与条件地公开您修改后的内容，并按指定的方式向此项目的维护者发送通知。指定的通知发送方式为 GitHub Issue 或向 support@lty.vc 发送电子邮件。您应在通知中包含您公开修改后内容的地址。您的修改仅限于向数据库中加入虚拟歌手为原唱演唱的中文歌曲，不得加入其他类型的歌曲，亦不得删除数据库中的条目。
 8. 免责声明。此项目的贡献者不对此项目及其产物的安全性、适用性、适销性提供任何明示或暗示的担保与保证。无论用户以何种方式使用此项目及其产物，作者均不对其用户使用此项目及其产物说造成的损害、责任赔偿、人身伤害或任何其他后果负责。
 9. bang15便士条款。无论因何种情况，此项目的贡献者对任何人拥有法定的求偿或追索的权利，其金额止于 9 英镑 15 便士。
