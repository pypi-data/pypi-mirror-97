# **************************************************************************** #
#                           This file is part of:                              #
#                                   METTLE                                     #
#                           https://bitsmiths.co.za                            #
# **************************************************************************** #
#  Copyright (C) 2015 - 2021 Bitsmiths (Pty) Ltd.  All rights reserved.        #
#   * https://bitbucket.org/bitsmiths_za/mettle.git                            #
#                                                                              #
#  Permission is hereby granted, free of charge, to any person obtaining a     #
#  copy of this software and associated documentation files (the "Software"),  #
#  to deal in the Software without restriction, including without limitation   #
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#  and/or sell copies of the Software, and to permit persons to whom the       #
#  Software is furnished to do so, subject to the following conditions:        #
#                                                                              #
#  The above copyright notice and this permission notice shall be included in  #
#  all copies or substantial portions of the Software.                         #
#                                                                              #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
#  DEALINGS IN THE SOFTWARE.                                                   #
# **************************************************************************** #
import datetime

from .statement import Statement


class IAConnect:
    """
    Interface for an async database connection object.
    """

    STMNT_TYPE_NA   = 0
    STMNT_TYPE_READ = 1
    STMNT_TYPE_CUD  = 2  # Create, Update, Delete


    def name(self) -> str:
        """
        The name of this database connection.

        :return: The name of this database connection.
        """
        pass


    async def commit(self):
        """
        Performs a database commit.
        """
        pass


    async def rollback(self):
        """
        Performs a database rollback.
        """
        pass


    async def fetch(self, stmnt: Statement) -> bool:
        """
        Fetches the next row from the statement object.

        :param stmnt: The database statement.
        :return: True if a row was fetched.
        """
        pass


    async def execute(self, stmnt: Statement):
        """
        Executes the provided statement.

        :param stmnt: The statement to be executed.
        """
        pass


    async def pre_get_sequence(self, stmtn: Statement, table: str, col: str, size: int) -> int:
        """
        Gets the next sequence number from the table if the database prior to insert.

        :param stmnt: The database statement.
        :param table: The name of the table's who's sequence to get.
        :param col: The name of the column for the on the table of who's sequence to get.
        :param size: The sequence size, ie 4 for in32, 8 for int64
        :return: The sequence number if the next sequence was retreieved, else returns None or raises an
                 exception if this database instead gets sequence's post insert.
        """
        pass


    async def post_get_sequence(self, stmnt: Statement, table: str, col: str, size: int) -> int:
        """
        Gets the next sequence number from the table if the database post insert.

        param stmnt: The database statement.
        param table: The name of the table's who's sequence to get.
        param col: The name of the column for the on the table of who's sequence to get.
        param size: The sequence size, ie 4 for in32, 8 for int64
        :return: The sequence number if the next sequence was retreieved, else returns None or raises an exception
                 if this database instead gets sequence's pre insert.
        """
        pass


    async def get_timestamp(self) -> datetime.datetime:
        """
        Gets the current date & time from the database.

        :returns : The timestamp from the database.
        """
        pass


    async def lock(self):
        """
        Tell the database we are about to attempt a row lock.
        """
        pass


    async def statement(self, name: str, stmnt_type: int = 0) -> Statement:
        """
        Creates a new Statement object for this database connection.

        :param name: The name of the statment.
        :param stmnt_type: Optionally provide the statement type.
        :return: Note the calling object must free/destroy this object.
        """
        pass


    def date_4_sql_inject(self, src_date: datetime.date) -> str:
        """
        Converts a date object, into a query usable equivalent for this specific database.

        :param src_date: The source date to be converted into a query compatiable string.
        :return: The resultent sql injectiable date string.
        """
        pass


    def datetime_4_sql_inject(self, src_datetime: datetime.datetime) -> str:
        """
        Converts a datetime object, into a query usable equivalent for this specific database.

        :param src_datetime: The source datetime to be converted into a query compatiable string.
        :return: The resultent sql injectiable datetime string.
        """
        pass


    def transaction_mode_get(self) -> bool:
        """
        Gets the auto transaction mode setting from the connection.

        :return: True if db connection is in auto transaction mode."
        """
        pass


    def transaction_mode_set(self, mode: bool):
        """
        Sets the auto tranaction mode.

        :param mode: Turn the auto transaction mode on/off, not all db connectors support this.
        """
        pass
