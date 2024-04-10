# meduzzen-internship
fast_api

Installation

1. Open the command prompt (terminal) on your computer.

2. Navigate to the folder where you want to save the repository.

3. Clone the repository using the following command:

git clone https://github.com/zhenia-cyp/meduzzen-internship.git

4. Navigate into the cloned repository:

cd meduzzen-internship

5. Create a virtual environment:

python3 -m venv venv

6. Activate the virtual environment:

- For Windows:

  ```
  venv\Scripts\activate
  ```

- For Linux:

  ```
  source venv/bin/activate
  ```

7. Install dependencies:

pip install -r requirements.txt


### Running the Application


 Run the following command:

uvicorn app.main:app --reload --env-file .env


### Running the Tests

Navigate to the project root directory meduzzen-internship/ and execute the command pytest
