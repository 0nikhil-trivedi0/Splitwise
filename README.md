# SplitWise(Expense Sharing Application)

## Overview
This project is an implementation of an Expense Sharing Application, a utility tool designed to help groups of individuals, such as friends or colleagues, manage and split their shared expenses efficiently. The application is developed using Python, leveraging the Flask framework, and utilizes MongoDB as its database.

## Features
- **User Management:** Allows adding and removing users, each with unique details like email and mobile number.
- **Expense Management:** Enables the creation and deletion of expenses, with details like amount, payer, and split type.
- **Split Types:** Supports EQUAL, EXACT, and PERCENT splits, allowing flexible expense sharing among participants.
- **Balance Management:** Maintains the balance between users, reflecting debts and settlements accurately.
- **Adjustment Handling:** Flags expenses that require adjustments due to user removals and recalculates the owed amounts or percentages accordingly.
- **Notifications:** Provides activity notifications to users, ensuring transparency in transactions and adjustments.

## Structure
The project is organized into modular components, each serving distinct responsibilities:
- **Models:** Contains classes and logic for Users and Expenses.
- **DB:** Holds MongoDB functions for User and Expense operations.
- **Routes:** Defines API endpoints for User and Expense management.
- **Docs:** Includes the MongoDB schema and other documentation.

## Setup and Run
1. Clone the repository to your local machine.
2. Install the required packages using pip:
   pip install -r requirements.txt
