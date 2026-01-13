import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import re
import os

class CSUSTSystem:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "http://xk.csust.edu.cn"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'http://xk.csust.edu.cn/',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    
    def get_encryption_params(self):
        """获取加密参数 scode 和 sxh"""
        url = f"{self.base_url}/Logon.do?method=logon&flag=sess"
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.text
                if "#" in data:
                    scode, sxh = data.split("#")
                    return scode, sxh
            return None, None
        except Exception as e:
            print(f"获取加密参数失败: {e}")
            return None, None
    
    def encrypt_password(self, username, password, scode, sxh):
        """按照前端逻辑加密账号密码"""
        code = username + "%%%" + password
        encoded = ""
        
        for i in range(len(code)):
            if i < 20:
                # 获取要插入的字符数
                insert_count = int(sxh[i])
                # 在当前位置后插入随机字符
                encoded += code[i] + scode[:insert_count]
                # 移除已使用的随机字符
                scode = scode[insert_count:]
            else:
                # 超过20位的部分直接拼接
                encoded += code[i:]
                break
        
        return encoded
    
    def get_verify_code(self, show_image=True):
        """获取验证码图片"""
        url = f"{self.base_url}/verifycode.servlet"
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                if show_image:
                    # 显示验证码图片
                    image = Image.open(io.BytesIO(response.content))
                    image.show()
                
                # 保存验证码图片（可选）
                with open('verify_code.png', 'wb') as f:
                    f.write(response.content)
                
                return True
            return False
        except Exception as e:
            print(f"获取验证码失败: {e}")
            return False
    
    def login(self, username, password, verify_code):
        """执行登录"""
        # 1. 获取加密参数
        scode, sxh = self.get_encryption_params()
        if not scode or not sxh:
            print("无法获取加密参数")
            return False
        
        print(f"获取到加密参数: scode={scode[:10]}..., sxh={sxh}")
        
        # 2. 加密账号密码
        encoded_password = self.encrypt_password(username, password, scode, sxh)
        print(f"加密后的密码长度: {len(encoded_password)}")
        
        # 3. 准备登录数据
        login_data = {
            'method': 'logon',
            'userAccount': '',  # 前端会清空这个字段
            'userPassword': '', # 前端会清空这个字段
            'RANDOMCODE': verify_code,
            'encoded': encoded_password
        }
        
        # 4. 提交登录请求
        login_url = f"{self.base_url}/Logon.do"
        try:
            response = self.session.post(
                login_url, 
                data=login_data, 
                headers=self.headers,
                allow_redirects=True
            )
            
            # 检查登录是否成功
            if response.status_code == 200:
                success_indicators = [
                    "教学一体化服务平台",
                    "mainFrame",
                    "sidebar-menu", 
                    "xsMain_new.jsp",
                    "个人中心"
                ]
                
                # 检查是否有错误信息
                if "用户名或密码错误" in response.text:
                    print("登录失败: 用户名或密码错误")
                    return False
                elif "验证码错误" in response.text:
                    print("登录失败: 验证码错误")
                    return False
                # 检查是否有成功特征
                elif any(indicator in response.text for indicator in success_indicators):
                    print("登录成功!")
                    # 保存session用于后续请求
                    return True
                else:
                    print("登录状态不确定")
                    return False
            else:
                print(f"登录请求失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"登录过程中发生错误: {e}")
            return False
    
    def auto_login_with_retry(self, username, password, max_retry=3):
        """自动登录（包含验证码重试）"""
        for attempt in range(max_retry):
            print(f"\n=== 第 {attempt + 1} 次登录尝试 ===")
            
            # 获取验证码图片
            if not self.get_verify_code(show_image=True):
                print("无法获取验证码")
                continue
            
            # 手动输入验证码
            verify_code = input("请输入验证码: ").strip()
            
            # 执行登录
            if self.login(username, password, verify_code):
                return True
            else:
                print("登录失败，准备重试...")
        
        print("超过最大重试次数，登录失败")
        return False

    def get_course_schedule_directly(self, academic_year="2025-2026-1", week=""):
        """直接获取课表数据，避免iframe问题"""
        # 直接访问课表页面的真实URL
        url = f"{self.base_url}/jsxsd/xskb/xskb_list.do"
        
        # 准备参数
        params = {
            'xnxq01id': academic_year,
            'zc': week
        }
        
        # 设置正确的headers
        headers = self.headers.copy()
        headers['Referer'] = f"{self.base_url}/jsxsd/framework/xsMain_new.jsp"
        
        try:
            response = self.session.get(url, params=params, headers=headers)
            if response.status_code == 200:
                print("成功获取课表页面")
                
                # 保存原始HTML用于调试
                with open('course_schedule_direct.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                return self.parse_course_schedule(response.text)
            else:
                print(f"请求课表失败，状态码: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取课表失败: {e}")
            return None

    def parse_course_schedule(self, html_content):
        """解析课表HTML内容"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找课表表格
        course_table = soup.find('table', {'class': 'Nsb_r_list Nsb_table'})
        
        if not course_table:
            print("未找到课表数据")
            # 保存HTML用于调试
            with open('debug_course_table.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            return None
        
        courses = []
        
        # 解析表格行
        rows = course_table.find_all('tr')
        
        for row in rows:
            # 获取所有单元格
            cells = row.find_all(['td', 'th'])
            if cells:
                # 提取单元格文本
                row_data = []
                for cell in cells:
                    # 处理课程单元格（包含kbcontent1 div）
                    kbcontent = cell.find('div', {'class': 'kbcontent1'})
                    if kbcontent:
                        # 提取课程信息
                        course_text = kbcontent.get_text(strip=True)
                        if course_text and course_text != '&nbsp;':
                            row_data.append(course_text)
                        else:
                            row_data.append("")
                    else:
                        # 普通单元格（时间、表头等）
                        cell_text = cell.get_text(strip=True)
                        row_data.append(cell_text)
                
                courses.append(row_data)
        
        return courses

    def format_course_schedule_markdown(self, courses):
        """以Markdown表格格式显示课表"""
        if not courses:
            print("没有课程数据")
            return
        
        print("\n# 学期理论课表\n")
        
        # 定义时间段
        time_slots = [
            '第一大节 08:00-09:40',
            '第二大节 10:10-11:50', 
            '第三大节 14:00-15:40',
            '第四大节 16:10-17:50',
            '第五大节 19:30-21:10'
        ]
        
        # 创建Markdown表格
        markdown_table = []
        
        # 表头
        markdown_table.append("| 时间 | 周一 | 周二 | 周三 | 周四 | 周五 | 周六 | 周日 |")
        markdown_table.append("|------|------|------|------|------|------|------|------|")
        
        # 处理每一行的课程数据（跳过表头行和备注行）
        for i in range(1, min(6, len(courses))):
            row = courses[i]
            time_display = time_slots[i-1] if i-1 < len(time_slots) else ""
            
            # 提取每天的课程（跳过第一列的时间信息）
            # 注意：HTML中的顺序是：时间, 周日, 周一, 周二, 周三, 周四, 周五, 周六
            # 我们要调整为：时间, 周一, 周二, 周三, 周四, 周五, 周六, 周日
            day_courses = []
            if len(row) > 7:
                # 重新排序：时间, 周一, 周二, 周三, 周四, 周五, 周六, 周日
                day_courses = [
                    row[2] if len(row) > 2 else "",  # 周一
                    row[3] if len(row) > 3 else "",  # 周二
                    row[4] if len(row) > 4 else "",  # 周三
                    row[5] if len(row) > 5 else "",  # 周四
                    row[6] if len(row) > 6 else "",  # 周五
                    row[7] if len(row) > 7 else "",  # 周六
                    row[1] if len(row) > 1 else ""   # 周日
                ]
            else:
                day_courses = [""] * 7
            
            # 格式化每门课程
            formatted_courses = []
            for course in day_courses:
                if course and course.strip():
                    clean_course = self.extract_course_info_markdown(course)
                    formatted_courses.append(clean_course)
                else:
                    formatted_courses.append("")
            
            # 构建表格行
            table_row = f"| {time_display} | {formatted_courses[0]} | {formatted_courses[1]} | {formatted_courses[2]} | {formatted_courses[3]} | {formatted_courses[4]} | {formatted_courses[5]} | {formatted_courses[6]} |"
            markdown_table.append(table_row)
        
        # 输出Markdown表格
        for line in markdown_table:
            print(line)
        
        # 输出详细信息
        print("\n## 课程详细信息\n")
        self.display_course_details(courses)
    
    def extract_course_info_markdown(self, course_text):
        """从课程文本中提取关键信息，格式化为Markdown"""
        # 分割多个课程
        courses = course_text.split('----------------------')
        
        clean_courses = []
        for course in courses:
            if course.strip():
                clean_info = self.parse_single_course_markdown(course)
                clean_courses.append(clean_info)
        
        return "<br>".join(clean_courses)
    
    def parse_single_course_markdown(self, course_text):
        """解析单门课程信息，格式化为Markdown"""
        # 使用正则表达式提取信息
        lines = [line.strip() for line in course_text.split('<br/>') if line.strip()]
        
        if not lines:
            return ""
        
        course_name = lines[0]
        
        # 提取周次信息
        week_info = ""
        for line in lines:
            if '周)' in line and '(' in line:
                week_match = re.search(r'\(([^)]+周)\)', line)
                if week_match:
                    week_info = week_match.group(1)
                    break
        
        # 提取教室信息
        classroom = ""
        for line in lines:
            if '金' in line and '-' in line:
                classroom_match = re.search(r'(金[\dA-Z]+-[\d]+)', line)
                if classroom_match:
                    classroom = classroom_match.group(1)
                    break
        
        # 组合信息
        result = f"**{course_name}**"
        if week_info:
            result += f" ({week_info})"
        if classroom:
            result += f"<br>@{classroom}"
        
        return result
    
    def display_course_details(self, courses):
        """显示课程详细信息"""
        all_courses = []
        
        # 时间段映射
        time_slots = [
            '08:00-09:40',
            '10:10-11:50', 
            '14:00-15:40',
            '16:10-17:50',
            '19:30-21:10'
        ]
        
        # 星期映射（HTML中的顺序）
        weekday_map = {
            1: '周日',
            2: '周一', 
            3: '周二',
            4: '周三',
            5: '周四',
            6: '周五',
            7: '周六'
        }
        
        # 收集所有课程
        for i in range(1, min(6, len(courses))):
            row = courses[i]
            for j in range(1, min(8, len(row))):
                course = row[j]
                if course and course.strip():
                    weekday = weekday_map.get(j, '')
                    time_slot = time_slots[i-1] if i-1 < len(time_slots) else ""
                    
                    # 解析课程
                    courses_list = course.split('----------------------')
                    for single_course in courses_list:
                        if single_course.strip():
                            clean_info = self.parse_single_course_markdown(single_course)
                            if clean_info:
                                all_courses.append(f"- **{weekday} {time_slot}**: {clean_info}")
        
        # 按星期排序输出
        weekday_order = {'周一': 0, '周二': 1, '周三': 2, '周四': 3, '周五': 4, '周六': 5, '周日': 6}
        all_courses.sort(key=lambda x: (weekday_order.get(x.split()[1], 7), x))
        
        for course in all_courses:
            # 移除HTML标签用于纯文本显示
            clean_course = re.sub(r'<[^>]+>', '', course)
            clean_course = re.sub(r'\*\*', '**', clean_course)  # 保留加粗标记
            print(clean_course)
    
    def display_course_schedule(self, courses):
        """以Markdown表格形式显示课表"""
        if not courses:
            print("没有课程数据")
            return
        
        self.format_course_schedule_markdown(courses)


# 使用示例
if __name__ == "__main__":
    system = CSUSTSystem()
    
    # 输入账号密码
    username = input("请输入账号: ")
    password = input("请输入密码: ")
    
    # 执行自动登录
    success = system.auto_login_with_retry(username, password)
    
    if success:
        print("\n登录成功！开始查询课表...")
        
        # 直接获取课表数据，避免iframe问题
        courses = system.get_course_schedule_directly()
        
        if courses:
            system.display_course_schedule(courses)
        else:
            print("获取课表失败，请检查网络连接或课程页面是否有变化")
    else:
        print("\n登录失败，请检查账号密码或网络连接")