# Astrbot 信息查询插件

![AstrbotPlugin-ProfileSearch](https://socialify.git.ci/QingFengTechnology/AstrbotPlugin-ProfileSearch/image?description=1&font=KoHo&language=1&name=1&pattern=Circuit+Board&theme=Auto)

> [!Warning]
> 本插件仅供学习交流，使用者不得用于非法或侵权行为，否则自行承担全部责任。\
> 本插件仅通过 Onebot 协议获取公开信息，插件所有者不对数据的准确性、完整性负责。\
> 不对魔改本插件（如接入社工库等违规操作）的行为负责，违者自行承担法律责任。\
> 使用者应自行评估使用风险，插件所有者不对使用过程中产生的任何损失或风险承担责任。\
> 本声明适用中华人民共和国法律，争议由插件所有者所在地法院管辖。\
> 插件所有者保留对本声明的最终解释权，并有权随时修改。


## 安装

在 Astrbot 应用市场点击右下角 + 号，选择`从链接安装`，复制粘贴本仓库 URL 并点击安装即可。

## 使用

- 自动开盒新群友（需在配置里添加群聊白名单）
- 指令调用：

```plaintext
/box [@目标]
/box [QQ号]
```

![33cd17b7bd27520aee2f463ff8a9d12](https://github.com/user-attachments/assets/97ffe26f-bf18-4cbe-93f4-1eb82e08edeb)

## 配置

```json
{
  "OnlyAdmin": {
    "description": "仅管理员可通过命令获取用户信息",
    "type": "bool", 
    "hint": "自己获取自己的信息不受该限制。",
    "default": false
  },
  "BoxBlacklist": {
    "description": "用户黑名单",
    "type": "list",
    "hint": "处于黑名单中的用户不会被通过/box命令获取到用户信息，这不影响自动获取用户信息。",
    "default": []
  },
  "WhitelistGroups": {
    "description": "群聊白名单",
    "type": "list",
    "default": [],
    "hint": "仅处理白名单群聊中的/box命令，留空则处理所有群聊的请求。"
  },
  "AutoBoxConfig": {
    "description": "自动获取配置",
    "type": "object",
    "items": {
      "AutoBoxConfig_IncreaseBox": {
        "description": "自动获取新进群的用户信息",
        "type": "bool",
        "default": false
      },
      "AutoBoxConfig_DecreaseBox": {
        "description": "自动获取退群用户的信息", 
        "type": "bool",
        "default": false
      },
      "AutoBoxConfig_WhiteGroups": {
        "description": "自动获取用户信息群聊白名单",
        "type": "list",
        "hint": "只自动获取用户信息白名单群聊的新群友/主动退群的用户，不填则所有群聊都启用自动获取用户信息。",
        "default": []
      }
    }
  },
  "RateLimitConfig": {
    "type": "object",
    "description": "速率限制配置",
    "items": {
      "RateLimitConfig_Time": {
        "description": "速率限制时间",
        "type": "int",
        "hint": "使用命令的最小间隔时间，单位为分钟，设为0表示不限制。",
        "default": 0
      },
      "RateLimitConfig_WhiteGroups": {
        "description": "群聊白名单",
        "type": "list",
        "hint": "白名单群聊不受速率限制。",
        "default": []
      },
      "RateLimitConfig_WhiteUsers": {
        "description": "用户白名单",
        "type": "list",
        "hint": "白名单用户在任何群聊中都不受速率限制。",
        "default": []
      }
    }
  }
}
```

## 鸣谢

- [Zhalslar](https://github.com/Zhalslar)，此插件为[其仓库](https://github.com/Zhalslar/astrbot_plugin_box)的分叉版本。