import os
import sys
import datetime as dt

from PyQt5.QtWidgets import *
from PyQt5 import uic

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = uic.loadUiType(resource_path('../ui/register.ui'))[0]
form2 = uic.loadUiType(resource_path('../ui/borrow.ui'))[0]


class Register(QMainWindow, form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

    def login(self): # 로그인 버튼 클릭
        self.close()
        self.borrow = Borrow(self.id_lineEdit.text())

    def signIn(self): # 등록 버튼 클릭
        pass


class Borrow(QDialog, QWidget, form2):
    def __init__(self, id):
        super(Borrow, self).__init__()
        self.setupUi(self)

        # 멤버 변수
        id = 'asdf' # tmp
        self.id = id
        self.bookList = self.createBookList()
        self.idInfo = self.createIdInfo(id)

        self.refreshTable()
        self.show()

    def borrowBook(self): # 대출 버튼 클릭
        borrowing_book = self.bookList.getBookInfo(self.bookCode_lineEdit.text())
        if borrowing_book[1] == False or borrowing_book[2] == 'borrowed': return

        self.idInfo.borrowBook(borrowing_book)
        self.bookList.borrowBook(borrowing_book)

        self.refreshTable()
        self.close()
        self.__init__(self.id)

    def returnBook(self): # 반납 버튼 클릭
        returning_book = [i.text() for i in self.idInfo_tableWidget.selectedItems()]
        self.idInfo.returnBook(returning_book)
        self.bookList.returnBook(returning_book)

        self.refreshTable()
        self.close()
        self.__init__(self.id)

    def extensionBook(self): # 연장 버튼 클릭
        extensioning_book = [i.text() for i in self.idInfo_tableWidget.selectedItems()]
        self.idInfo.extensionBook(extensioning_book)

        self.refreshTable()
        self.close()
        self.__init__(self.id)

    def leave(self): # 종료 버튼 클릭
        print('leave')
        self.close()
        self.register = Register()

    def createBookList(self): # BookList class 생성
        return BookList()

    def createIdInfo(self, id): # IdInfo Class 생성
        return IdInfo(id)

    def refreshTable(self): # 테이블 갱신
        for r in range(len(self.idInfo.idInfoArr)):
            for c in range(4):
                tableItem = QTableWidgetItem()
                tableItem.setText(self.idInfo.idInfoArr[r][c])
                self.idInfo_tableWidget.setItem(r, c, tableItem)


class IdInfo:
    def __init__(self, id):
        # 멤버 변수
        self.id = id
        self.idInfoArr = []

        self.getIdInfo()

    def getIdInfo(self): # 대출 목록 갱신
        with open(f'../data/idInfo/{self.id}.txt', 'r', encoding="UTF-8") as f:
            for line in f:
                book = line.split()
                self.idInfoArr.append(book)

    def borrowBook(self, borrowing_book): # 대출 버튼 클릭
        date = dt.datetime.today() + dt.timedelta(weeks=1)
        dateStr = dt.datetime.strftime(date, '%Y/%m/%d')

        with open(f'../data/idInfo/{self.id}.txt', 'a', encoding="UTF-8") as f:
            f.write(borrowing_book[0] + ' ')
            f.write(borrowing_book[1] + ' ')
            f.write(dateStr + ' ')
            f.write('X' + '\n')

    def returnBook(self, returning_book): # 반납 버튼 클릭
        self.idInfoArr.remove(returning_book)

        with open(f'../data/idInfo/{self.id}.txt', 'w', encoding="UTF-8") as f:
            for book in self.idInfoArr:
                f.write(book[0] + ' ')
                f.write(book[1] + ' ')
                f.write(book[2] + ' ')
                f.write(book[3] + '\n')

    def extensionBook(self, extensioning_book): # 연장 버튼 클릭
        if extensioning_book[3] == 'O': return
        try: idx = self.idInfoArr.index(extensioning_book)
        except: return

        date = dt.datetime.strptime(extensioning_book[2], '%Y/%m/%d') + dt.timedelta(weeks=1)
        dateStr = dt.datetime.strftime(date, '%Y/%m/%d')
        self.idInfoArr[idx] = [extensioning_book[0], extensioning_book[1], dateStr, 'O']

        with open(f'../data/idInfo/{self.id}.txt', 'w', encoding="UTF-8") as f:
            for book in self.idInfoArr:
                f.write(book[0] + ' ')
                f.write(book[1] + ' ')
                f.write(book[2] + ' ')
                f.write(book[3] + '\n')


class BookList:
    def __init__(self):
        # 멤버 변수
        self.bookListArr = []

        with open('../data/BookList.txt', 'r', encoding="UTF-8") as f:
            for line in f:
                book = line.split()
                self.bookListArr.append(book)

    def getBookInfo(self, code): # 책 정보 반환
        name = False
        status = False
        for book in self.bookListArr:
            if book[0] == code:
                name = book[1]
                status = book[2]
                break

        return [code, name, status]

    def borrowBook(self, borrowing_book): # 대출 버튼 클릭
        try: idx = self.bookListArr.index(borrowing_book)
        except: return
        self.bookListArr[idx] = [borrowing_book[0], borrowing_book[1], 'borrowed']

        with open('../data/BookList.txt', 'w', encoding="UTF-8") as f:
            for book in self.bookListArr:
                f.write(book[0] + ' ')
                f.write(book[1] + ' ')
                f.write(book[2] + '\n')

    def returnBook(self, returning_book): # 반납 버튼 클릭
        idx = self.bookListArr.index([returning_book[0], returning_book[1], 'borrowed'])
        self.bookListArr[idx] = [returning_book[0], returning_book[1], 'ready']

        with open('../data/BookList.txt', 'w', encoding="UTF-8") as f:
            for book in self.bookListArr:
                f.write(book[0] + ' ')
                f.write(book[1] + ' ')
                f.write(book[2] + '\n')


# class IdList:
#     def __init__(self):
#         # 멤버 변수
#         self.IdListFile = open('../data/IdList.txt', 'r', encoding="UTF-8")
#         self.idListArr = []


if __name__ == '__main__':
    app = QApplication(sys.argv)
    register = Register()
    sys.exit(app.exec())
