import re
import sys
import secrets
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDialog, QHBoxLayout, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt
from eth_account import Account
import requests

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QMessageBox
from PyQt5.QtGui import QDesktopServices, QIcon


class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('帮助说明')

        # 创建布局
        layout = QVBoxLayout()

        # 说明内容
        help_text = QLabel(
            """<b>欢迎使用以太坊钱包生成器！</b><br><br>
            1. 输入您希望生成的私钥数量。<br>
            2. 点击‘生成私钥和地址’按钮来生成您的钱包。<br>
            3. 生成的私钥和地址将保存在当前目录下的文件中。<br>
            4. 通过输入钱包地址，您可以查询到对应的私钥；反之亦然。<br><br>

            <b>🔑 安全提示</b><br>
            私钥是您钱包的唯一凭证，丢失后无法恢复，请务必妥善保存！<br><br>

            <b>❓ 常见问题</b><br>
            <b>Q1:</b> 如何获取生成的文件？<br>
            <b>A1:</b> 文件会保存到当前程序所在的目录，您可以通过文件管理器查看。<br><br>

            <b>Q2:</b> 如果私钥丢失，如何找回？<br>
            <b>A2:</b> 私钥一旦丢失，无法找回，请确保保存备份。<br><br>

            <b>Q3:</b> 如何使用私钥恢复钱包？<br>
            <b>A3:</b> 您可以在支持以太坊的钱包软件中使用私钥导入钱包。<br><br>

            <b>Q4:</b> 如何验证生成的钱包地址的安全性？<br>
            <b>A4:</b> 请确保在可信环境中生成钱包，避免使用未授权的软件或服务。<br><br>

            <b>📞 联系方式</b><br>
            如果您有任何问题或建议，欢迎通过以下方式与我联系：<br>
            - 推特 (Twitter): <a href="https://twitter.com/OxStackCoder" target="_blank" id="twitter-link"> OxStackCoder </a><br>
            - 微信 (WeChat): <a href="weixin://dl/chat?chatid=Code-love" target="_blank" id="wechat-link"> Code-love </a><br><br>

            <b>🚀 软件更新</b><br>
            本软件会不定期进行更新，加入更多新功能和优化。<br>
            为了不漏掉重要更新，建议您关注我们的推特账号或添加微信，以便及时获取最新消息和技术支持。<br>
            加入我们，您不仅可以获得更新信息，还能参与更多的社区互动哦！<br><br>

            <b>⚖️ 法律免责声明</b><br>
            本软件仅供个人学习、研究和开发使用。用户在使用本软件时，需自行承担所有责任，包括但不限于因使用本软件产生的任何经济损失、数据丢失或其他法律责任。<br>
            本软件不对任何因使用本软件而产生的后果负责。用户在使用本软件前应确保自己完全理解软件功能及其风险。<br>
            本软件不得用于任何非法活动，包括但不限于未经授权的访问、数据盗用等行为。用户在使用过程中，应遵循所有适用的法律法规，确保自己的行为合法合规。<br><br>

            <b>🔐 关于隐私与安全</b><br>
            本软件承诺没有任何后门，所有生成的私钥和钱包地址仅保存在本地，不会上传到任何服务器或第三方服务。我们绝不会收集您的个人信息或任何加密数据。<br><br>

            <b>🔓 开源声明</b><br>
            本软件的源代码完全开源，您可以在GitHub上查看和修改代码。我们鼓励您在使用软件时参与贡献，任何修改后的版本都应遵循开源协议。我们坚信开源是保障软件透明度和安全性的关键，用户可以通过查看源代码验证我们的承诺。<br><br>

            <b>💻 源代码地址</b><br>
            请访问我们的GitHub页面，查看源代码并参与开发和改进：<br>
            - GitHub: <a href="https://github.com/OxStackCoder/ethereum-wallet-generator" target="_blank">Ethereum钱包生成器 - GitHub</a><br><br>
            """,
            self
        )

        layout.addWidget(help_text)

        # 按钮区
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        layout.addWidget(buttons)

        # 设置布局
        self.setLayout(layout)
        buttons.accepted.connect(self.accept)

        # Connect links
        help_text.linkActivated.connect(self.handle_link_click)

    def handle_link_click(self, link):
        if "twitter.com" in link:
            # 打开Twitter链接
            QDesktopServices.openUrl(QUrl(link))
            self.show_message("成功复制推特链接到剪贴板！")
        elif "weixin://" in link:
            # 打开微信链接
            QDesktopServices.openUrl(QUrl(link))
            self.show_message("成功复制微信链接到剪贴板！")

    def show_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("复制成功")
        msg.exec_()


class EthereumWalletGenerator(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化界面组件
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Ethereum钱包生成器')
        # 设置窗口图标
        # 获取当前脚本所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))

        # 构建图标文件的绝对路径
        icon_path = os.path.join(base_path, 'ethereum.ico')
        self.setWindowIcon(QIcon(icon_path))  # 这里传入你的图标文件路径
        self.setGeometry(100, 100, 450, 600)


        # 创建主布局
        self.layout = QVBoxLayout()

        # 标题
        self.title_label = QLabel('Ethereum钱包生成器', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.title_label)

        # 生成私钥数量输入框
        self.num_keys_input = QLineEdit(self)
        self.num_keys_input.setPlaceholderText("请输入要生成的私钥数量")
        self.num_keys_input.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 5px; border: 1px solid #ddd;")
        self.layout.addWidget(self.num_keys_input)

        # 生成私钥和地址按钮
        self.generate_button = QPushButton('生成私钥和地址', self)
        self.generate_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 12px; font-size: 16px; border-radius: 8px;")
        self.generate_button.clicked.connect(self.generate_keys_and_addresses)
        self.layout.addWidget(self.generate_button)

        # 查找私钥功能区
        self.find_private_key_button = QPushButton('根据地址查找私钥', self)
        self.find_private_key_button.setStyleSheet("background-color: #2196F3; color: white; padding: 12px; font-size: 16px; border-radius: 8px;")
        self.find_private_key_button.clicked.connect(self.find_private_key_by_address)
        self.layout.addWidget(self.find_private_key_button)

        # 查找地址功能区
        self.find_address_button = QPushButton('根据私钥查找地址', self)
        self.find_address_button.setStyleSheet("background-color: #2196F3; color: white; padding: 12px; font-size: 16px; border-radius: 8px;")
        self.find_address_button.clicked.connect(self.find_address_by_private_key)
        self.layout.addWidget(self.find_address_button)

        # 输入框：根据地址查找私钥
        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText("请输入以太坊地址")
        self.address_input.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 5px; border: 1px solid #ddd;")
        self.layout.addWidget(self.address_input)

        # 输入框：根据私钥查找地址
        self.private_key_input = QLineEdit(self)
        self.private_key_input.setPlaceholderText("请输入以太坊私钥")
        self.private_key_input.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 5px; border: 1px solid #ddd;")
        self.layout.addWidget(self.private_key_input)

        # 结果显示区域：多行文本框
        self.result_input = QTextEdit(self)
        self.result_input.setPlaceholderText("结果显示在这里...")
        self.result_input.setReadOnly(True)
        self.result_input.setStyleSheet("padding: 10px; font-size: 14px; border-radius: 5px; border: 1px solid #ddd;")
        self.layout.addWidget(self.result_input)

        # 复制结果按钮
        self.copy_button = QPushButton('复制私钥或地址', self)
        self.copy_button.setStyleSheet("background-color: #FF9800; color: white; padding: 12px; font-size: 16px; border-radius: 8px;")
        self.copy_button.clicked.connect(self.copy_result_to_clipboard)
        self.layout.addWidget(self.copy_button)

        # 帮助按钮
        self.help_button = QPushButton('帮助', self)
        self.help_button.setStyleSheet("background-color: #8E24AA; color: white; padding: 12px; font-size: 16px; border-radius: 8px;")
        self.help_button.clicked.connect(self.show_help)
        self.layout.addWidget(self.help_button)

        # 设置主布局
        self.setLayout(self.layout)

    def show_help(self):
        help_window = HelpWindow()
        help_window.exec_()

    def generate_private_keys(self, num_keys=10):
        Account.enable_unaudited_hdwallet_features()

        private_keys = []
        for _ in range(num_keys):
            private_key = secrets.token_hex(32)
            private_keys.append(private_key)

        return private_keys

    def extract_addresses(self, private_keys):
        Account.enable_unaudited_hdwallet_features()

        addresses = []
        for private_key in private_keys:
            account_key = '0x' + private_key if not private_key.startswith('0x') else private_key
            account = Account.from_key(account_key)
            addresses.append(account.address)

        return addresses

    def save_to_file(self, private_keys, addresses):
        try:
            current_directory = os.getcwd()

            private_file_path = os.path.join(current_directory, 'private_keys.txt')
            address_file_path = os.path.join(current_directory, 'addresses.txt')

            with open(private_file_path, 'w') as f:
                for private_key in private_keys:
                    f.write(f'0x{private_key}\n')

            with open(address_file_path, 'w') as f:
                for address in addresses:
                    f.write(f'{address}\n')

            return private_file_path, address_file_path
        except Exception as e:
            self.result_input.setText(f'保存文件时发生错误: {str(e)}')
            return None, None

    def generate_keys_and_addresses(self):
        try:
            num_keys = int(self.num_keys_input.text())
            if num_keys <= 0:
                self.result_input.setText('请输入有效的私钥数量。')
                return

            self.generate_button.setDisabled(True)
            private_keys = self.generate_private_keys(num_keys)
            addresses = self.extract_addresses(private_keys)
            private_file, address_file = self.save_to_file(private_keys, addresses)

            if private_file and address_file:
                self.result_input.setText(f'成功生成了 {num_keys} 个私钥和地址。\n\n文件已保存至当前目录：\n{private_file}\n{address_file}')
            else:
                self.result_input.setText('文件保存失败，请重试。')

        except ValueError:
            self.result_input.setText('请输入有效的数字。')
        except Exception as e:
            self.result_input.setText(f'发生错误: {str(e)}')
        finally:
            self.generate_button.setEnabled(True)

    def find_private_key_by_address(self):
        address = self.address_input.text()
        try:
            with open('addresses.txt', 'r') as f:
                addresses = f.readlines()

            if address + '\n' in addresses:
                index = addresses.index(address + '\n')

                with open('private_keys.txt', 'r') as f:
                    private_keys = f.readlines()

                private_key = private_keys[index].strip()
                self.result_input.setText(f'对应的私钥是：{private_key}')
            else:
                self.result_input.setText('未找到对应的地址。')
        except FileNotFoundError:
            self.result_input.setText('文件未找到，请生成私钥和地址。')

    def find_address_by_private_key(self):
        private_key = self.private_key_input.text()
        try:
            with open('private_keys.txt', 'r') as f:
                private_keys = f.readlines()

            private_key_with_prefix = '0x' + private_key if not private_key.startswith('0x') else private_key
            if private_key_with_prefix + '\n' in private_keys:
                index = private_keys.index(private_key_with_prefix + '\n')

                with open('addresses.txt', 'r') as f:
                    addresses = f.readlines()

                address = addresses[index].strip()
                self.result_input.setText(f'对应的地址是：{address}')
            else:
                self.result_input.setText('未找到对应的私钥。')
        except FileNotFoundError:
            self.result_input.setText('文件未找到，请生成私钥和地址。')

    def copy_result_to_clipboard(self):
        clipboard = QApplication.clipboard()
        result_text = self.result_input.toPlainText()
        matches = re.findall(r'：\s*(\S+)', result_text)
        if matches:
            clipboard.setText(matches[-1])
        else:
            self.result_input.setText('没有可以复制的有效私钥或地址。')

def main():
    app = QApplication(sys.argv)
    window = EthereumWalletGenerator()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
