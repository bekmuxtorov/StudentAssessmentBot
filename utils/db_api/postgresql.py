from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE,
            full_name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20) NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_payments(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Payments (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            start_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_attempts(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Attempts (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            status VARCHAR(10) CHECK (status IN ('active', 'closed')),
            create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # USERS TABLE FUNCTIONS
    async def add_user(self, full_name, phone_number, telegram_id):
        sql = """
        INSERT INTO Users (full_name, phone_number, telegram_id)
        VALUES ($1, $2, $3) RETURNING *;
        """
        user = await self.execute(sql, full_name, phone_number, telegram_id, fetchrow=True)
        return {
            "id": user[0],
            "full_name": user[1],
            "phone_number": user[2],
            "telegram_id": user[3],
            "created_date": user[4],
        } if user else None

    async def select_all_users(self):
        sql = "SELECT * FROM Users;"
        users = await self.execute(sql, fetch=True)
        return [
            {
                "id": user[0],
                "full_name": user[1],
                "phone_number": user[2],
                "telegram_id": user[3],
                "created_date": user[4],
                "updated_date": user[5],
            } for user in users
        ] if users else []

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        user = await self.execute(sql, *parameters, fetchrow=True)
        return {
            "id": user[0],
            "full_name": user[1],
            "phone_number": user[2],
            "telegram_id": user[3],
            "created_date": user[4],
            "updated_date": user[5],
        } if user else None

    async def delete_user(self, telegram_id):
        sql = "DELETE FROM Users WHERE telegram_id = $1 RETURNING *;"
        user = await self.execute(sql, telegram_id, fetchrow=True)
        return {
            "id": user[0],
            "full_name": user[1],
            "phone_number": user[2],
            "telegram_id": user[3],
            "created_date": user[4],
            "updated_date": user[5],
        } if user else None

    # PAYMENTS TABLE FUNCTIONS
    async def add_payment(self, user_id, start_date, end_date, amount):
        sql = """
        INSERT INTO Payments (user_id, start_date, end_date, amount)
        VALUES ($1, $2, $3, $4) RETURNING *;
        """
        payment = await self.execute(sql, user_id, start_date, end_date, amount, fetchrow=True)
        return {
            "id": payment[0],
            "user_id": payment[1],
            "start_date": payment[2],
            "end_date": payment[3],
            "amount": payment[4],
            "created_date": payment[5],
        } if payment else None

    async def select_all_payments(self):
        sql = "SELECT * FROM Payments;"
        payments = await self.execute(sql, fetch=True)
        return [
            {
                "id": payment[0],
                "user_id": payment[1],
                "start_date": payment[2],
                "end_date": payment[3],
                "amount": payment[4],
                "created_date": payment[5],
            } for payment in payments
        ] if payments else []

    async def select_payment(self, **kwargs):
        sql = "SELECT * FROM Payments WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        payment = await self.execute(sql, *parameters, fetchrow=True)
        return {
            "id": payment[0],
            "user_id": payment[1],
            "start_date": payment[2],
            "end_date": payment[3],
            "amount": payment[4],
            "created_date": payment[5],
        } if payment else None

    async def delete_payment(self, payment_id):
        sql = "DELETE FROM Payments WHERE id = $1 RETURNING *;"
        payment = await self.execute(sql, payment_id, fetchrow=True)
        return {
            "id": payment[0],
            "user_id": payment[1],
            "start_date": payment[2],
            "end_date": payment[3],
            "amount": payment[4],
            "created_date": payment[5],
        } if payment else None

    # ATTEMPTS TABLE FUNCTIONS
    async def add_attempt(self, user_id, status):
        sql = """
        INSERT INTO Attempts (user_id, status)
        VALUES ($1, $2) RETURNING *;
        """
        attempt = await self.execute(sql, user_id, status, fetchrow=True)
        return {
            "id": attempt[0],
            "user_id": attempt[1],
            "status": attempt[2],
            "create_date": attempt[3],
        } if attempt else None

    async def select_all_attempts(self):
        sql = "SELECT * FROM Attempts;"
        attempts = await self.execute(sql, fetch=True)
        return [
            {
                "id": attempt[0],
                "user_id": attempt[1],
                "status": attempt[2],
                "create_date": attempt[3],
            } for attempt in attempts
        ] if attempts else []

    async def select_attempt(self, **kwargs):
        sql = "SELECT * FROM Attempts WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        attempt = await self.execute(sql, *parameters, fetchrow=True)
        return {
            "id": attempt[0],
            "user_id": attempt[1],
            "status": attempt[2],
            "create_date": attempt[3],
        } if attempt else None

    async def delete_attempt(self, attempt_id):
        sql = "DELETE FROM Attempts WHERE id = $1 RETURNING *;"
        attempt = await self.execute(sql, attempt_id, fetchrow=True)
        return {
            "id": attempt[0],
            "user_id": attempt[1],
            "status": attempt[2],
            "create_date": attempt[3],
        } if attempt else None
