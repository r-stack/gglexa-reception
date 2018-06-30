# SQS2GoogleHome

## Raspberry Pi のセットアップ

* Raspbian Stretch Lite をDL  
  https://www.raspberrypi.org/downloads/raspbian/

* EtcherをDL＆インストール  
  https://etcher.io/

* Etcherでイメージ(zipのままでOK)を焼く

* 焼いた後のSDカードのドライブを開き、最上位に`ssh`という名前のファイルを作成(空でOK)すると起動時にSSHができるようになる。

* 同じく、`wpa_supplicant.conf`を作成して以下を記述すると起動時に自動的にWiFiに繋がる。

> 改行コードは`LF`で。

```
country=JP
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
        ssid="----Your-WiFi-SSID----"
        psk="----PLAIN-PASSPHRASE----"
}
```

* Macはそのまま、Windowsなら[Bonjour](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)がインストールしてあれば、raspberrypi.local でSSH接続できるはず。

```
pi / raspberry
```

## AWS SDK と Google Home Notifier を利用するためのセットアップ 

* Nodeや関連パッケージのインストール  
  > curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -  
  > sudo apt-get install -y nodejs  
  > sudo apt-get install -y git-core libnss-mdns libavahi-compat-libdnssd-dev  


* `sqs2ghome`を`~/`などに配置して依存物をインストールする。
  > cd sqs2ghome
  > npm install

* MNDSのソース修正(ラズパイ用バグ対策)  
  > vi node_modules/mdns/lib/browser.js

```
Browser.defaultResolverSequence = [
  rst.DNSServiceResolve(), 'DNSServiceGetAddrInfo' in dns_sd ? rst.DNSServiceGetAddrInfo() : rst.getaddrinfo()
, rst.makeAddressesUnique()
];

↓

Browser.defaultResolverSequence = [
  rst.DNSServiceResolve(), 'DNSServiceGetAddrInfo' in dns_sd ? rst.DNSServiceGetAddrInfo() : rst.getaddrinfo({families:[4]})
, rst.makeAddressesUnique()
];
```

* 環境変数の設定  
  > export AWS_ACCESS_KEY_ID=XXXXXXXXXX  
  > export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXX  
    
  > SQS:ReceiveMessage と SQS:DeleteMessage の権限が必要

* 実行する。  
  > node main.js