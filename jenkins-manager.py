
import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException


class JenkinsClient:
    def __init__(self, url, username, token):
        self.url = url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, token)
        self.session.headers.update({
            "Accept": "application/json"
        })
        self.timeout = 15

    def _request(self, method, endpoint, **kwargs):
        """Wykonuje żądanie HTTP do Jenkins API."""
        url = f"{self.url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method,
                url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response

        except requests.exceptions.Timeout:
            print("[ERROR] Przekroczono czas oczekiwania.")
        except requests.exceptions.ConnectionError:
            print("[ERROR] Nie można połączyć się z Jenkins.")
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            print(f"[ERROR] HTTP {status}: {e}")
        except RequestException as e:
            print(f"[ERROR] Błąd komunikacji: {e}")

        return None

    def list_jobs(self):
        """Pobiera wszystkie zadania Jenkins."""
        response = self._request(
            "GET",
            "/api/json?tree=jobs[name,url,color]"
        )

        if not response:
            return []

        try:
            jobs = response.json().get("jobs", [])

            print("\n=== LISTA ZADAŃ ===")

            for job in jobs:
                print(
                    f"Nazwa: {job['name']} | "
                    f"Status: {job.get('color', 'UNKNOWN')} | "
                    f"URL: {job['url']}"
                )

            return jobs

        except (ValueError, KeyError) as e:
            print(f"[ERROR] Niepoprawna odpowiedź JSON: {e}")
            return []

    def get_last_build_status(self, job_name):
        """Sprawdza status ostatniego buildu zadania."""
        endpoint = (
            f"job/{job_name}/lastBuild/api/json"
            "?tree=number,result,building,timestamp,url"
        )

        response = self._request("GET", endpoint)

        if not response:
            return None

        try:
            build = response.json()

            status = (
                "BUILDING" if build.get("building")
                else build.get("result", "UNKNOWN")
            )

            print(f"\n=== OSTATNI BUILD: {job_name} ===")
            print(f"Numer: {build.get('number')}")
            print(f"Status: {status}")
            print(f"URL: {build.get('url')}")

            return build

        except ValueError as e:
            print(f"[ERROR] Niepoprawna odpowiedź JSON: {e}")
            return None

    def trigger_job(self, job_name):
        """Uruchamia wybrane zadanie Jenkins."""
        endpoint = f"job/{job_name}/build"

        response = self._request("POST", endpoint)

        if response is None:
            return False

        print(f"[OK] Zadanie '{job_name}' zostało uruchomione.")
        print(f"HTTP Status: {response.status_code}")

        return True


def main():
    url = os.getenv("JENKINS_URL")
    username = os.getenv("JENKINS_USER")
    token = os.getenv("JENKINS_TOKEN")

    if not all([url, username, token]):
        print("[ERROR] Brak konfiguracji Jenkins.")
        print("Ustaw JENKINS_URL, JENKINS_USER i JENKINS_TOKEN.")
        sys.exit(1)

    jenkins = JenkinsClient(url, username, token)

    while True:
        print("\n========== JENKINS MANAGER ==========")
        print("1. Lista wszystkich zadań")
        print("2. Status ostatniego buildu")
        print("3. Uruchom zadanie")
        print("4. Wyjście")

        choice = input("\nWybierz opcję: ").strip()

        if choice == "1":
            jenkins.list_jobs()

        elif choice == "2":
            job_name = input("Podaj nazwę zadania: ").strip()
            if job_name:
                jenkins.get_last_build_status(job_name)

        elif choice == "3":
            job_name = input("Podaj nazwę zadania: ").strip()
            if job_name:
                confirm = input(
                    f"Czy uruchomić '{job_name}'? (tak/nie): "
                ).strip().lower()

                if confirm == "tak":
                    jenkins.trigger_job(job_name)

        elif choice == "4":
            print("Zamykanie programu...")
            break

        else:
            print("[ERROR] Nieprawidłowa opcja.")


if __name__ == "__main__":
    main()
