import urllib.request as url
import tempfile
import shutil, os
from datetime import date, timedelta, datetime
import csv
import pathlib


class Vax_Stats:
    """Access and summarize Ohio COVID vaccine statistics.

    Provides functionality to retrieve and summarize Ohio COVID vaccine
        statistics from the Ohio Deparment of Health (ODH) website.

    Attributes:
        ODH_URL (string): URL for CSV vaccine data published by ODH.
        SELF_PATH (Path): Path to this file.
        POPULATION_PATH (Path): Path to population.csv.
        POPULATION (dict): List of Ohio counties and associated
            populations. Data is from the United States Census Bureau.
            Loaded from `population.csv`.
    """

    ODH_URL = "https://coronavirus.ohio.gov/static/dashboards/vaccine_data.csv"
    SELF_PATH = pathlib.Path(__file__).parent.absolute()
    POPULATION_PATH = SELF_PATH.joinpath("population.csv")
    POPULATION = {}

    def __init__(self) -> None:
        """Initialize vaccination data"""
        self._get_populations()
        self._get_odh_data()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.unlink(self.data_file.name)

    def _get_populations(self):
        """Load population data from population.csv"""
        with open(self.POPULATION_PATH, newline="") as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                self.POPULATION[row["county"]] = int(row["population"])

    def _get_odh_data(self):
        """Get vaccination data from ODH website"""
        req = url.Request(self.ODH_URL)
        with url.urlopen(req) as response:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                shutil.copyfileobj(response, tmp_file)
        self.data_file = tmp_file

    def _process_date(self, odh_date: str) -> date:
        """Convert ODH date into date object.

        Need a separate function because they keep changing the format.
        """
        formats = ["%m/%d/%Y", "%Y-%m-%d"]
        for f in formats:
            try:
                return datetime.strptime(odh_date, f).date()
            except ValueError:
                pass
        raise ValueError("ODH date format is not supported.")

    def odh_latest(self):
        """Find the latest date posted in ODH statistics"""
        latest = date(2020, 12, 14)
        with open(self.data_file.name, newline="") as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                p_date = self._process_date(row["date"])
                if p_date > latest:
                    latest = p_date
        return latest

    def lookup(
        self,
        county: str = "All",
        date: date = date.today(),
        cumulative: bool = True,
    ) -> tuple:
        """Lookup county data by date from ODH vaccination records.

        Args:
            county (str, optional): County name or "All" for entire
                state. Defaults to "All".
            date (date, optional): Date of data. Defaults to today.
            cumulative (bool, optional): Return cumulative data if True
            (default) or single-day data if False.

        Returns:
            tuple: (vaccines started, vaccines completed) where
                'vaccines started' indicates the number of people who
                received the first dose of COVID vaccine and 'vaccines
                completed' indicates the number who received their final
                dose.
        """
        totals = (0, 0)
        with open(self.data_file.name, newline="") as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                p_date = self._process_date(row["date"])
                if cumulative:
                    date_ok = p_date <= date
                else:
                    date_ok = p_date == date

                p_county = row["county"].rstrip()
                county_ok = p_county == county or county == "All"

                if county_ok and date_ok:
                    add = (
                        int(row["vaccines_started"]),
                        int(row["vaccines_completed"]),
                    )
                    totals = tuple(sum(x) for x in zip(totals, add))
        return totals

    def delta(
        self,
        county: str = "All",
        back_date: date = date.today() - timedelta(7),
        front_date: date = date.today(),
        percent: bool = True,
    ) -> tuple:
        """Find change in total vaccinations across two time points.

        Args:
            county (str, optional): County name or "All" for entire
                state. Defaults to "All".
            back_date (date, optional): Previous date to use for
                comparison. Defaults to one week ago.
            front_date (date, optional): More recent date to use for
                comparison. Defaults to today.
            percent (bool, optional): Return change as percentage if
                True (default) or integer if False.

        Returns:
            tuple: (change in vaccines started, change in vaccines
                completed) where 'vaccines started' indicates the number
                of people who received the first dose of COVID vaccine
                and 'vaccines completed' indicates the number who
                received their final dose.
        """
        q1, r1 = self.lookup(county, back_date)
        q2, r2 = self.lookup(county, front_date)
        if percent:
            d_started = round((q2 / q1 - 1) * 100, 1)
            d_completed = round((r2 / r1 - 1) * 100, 1)
        else:
            d_started = q2 - q1
            d_completed = r2 - r1
        return (d_started, d_completed)

    def percent_vaccinated(
        self,
        county: str = "All",
        date: date = date.today(),
        fully_vaccinated: bool = True,
    ) -> float:
        """Get percentage of total population vaccinated.

        Args:
            county (str, optional): County name or "All" for entire
                state. Defaults to "All".
            date (date, optional): Date of data. Defaults to today.
            fully_vaccinated (bool, optional): Count only people who
                received a full vaccination series if True (default).
                If False, count all people who received at least one
                vaccine even if they did not complete the series.

        Returns:
            float: Percent of population vaccinated (between 0 and 100).
        """
        n_partial, n_full = self.lookup(county, date)
        if fully_vaccinated:
            vaccinated = n_full
        else:
            vaccinated = n_partial
        return round(vaccinated / self.POPULATION[county] * 100, 1)

    def predict_herd_immunity(
        self,
        county: str = "All",
        back_date: date = date.today() - timedelta(7),
        front_date: date = date.today(),
        r_0: float = 2.5,
        started_efficacy: float = 0.5,
        full_efficacy: float = 0.95,
    ) -> date:
        """Predict at what point herd immunity will be reached.

        Args:
            county (str, optional): County name or "All" for entire
                state. Defaults to "All".
            back_date (date, optional): Previous date to use for
                vaccination rate calculation. Defaults to one week ago.
            front_date (date, optional): More recent date to use for
                vaccination rate calculation. Defaults to today.
            r_0 (float, optional): Reproductive number (sometimes
                referred to as "r naught"). Defaults to 2.5.
            started_efficacy (float, optional): Efficacy of vaccination
                after a single dose (between 0 and 1). Defaults to 0.5.
            full_efficacy (float, optional): Efficacy of vaccination
                after completing the vaccine series (between 0 and 1).
                Defaults to 0.95.

        Returns:
            date: Date prediction of herd immunity.

        Raises:
            ValueError: if herd immunity is impossible at current
                vaccination rates or is predicted to take longer than 2
                years.
        """
        # Calculate total number of currently vaccinated people
        n_started, n_full = self.lookup(county, front_date)
        n_started -= n_full  # Correct for completed series

        # Calculate the rates at which vaccinations are occurring
        d_started, d_full = self.delta(county, back_date, front_date, False)
        d_started -= d_full  # Rough estimate correction for completed series
        d_t = (front_date - back_date).days
        d_started /= d_t
        d_full /= d_t

        population = self.POPULATION[county]

        # Look forward up to two years
        days_to_herd_imm = 0
        for day in range(1, 731):
            n_started += d_started
            n_full += d_full

            if n_full + n_started > population:
                raise ValueError("No herd immunity at current rate.")

            # Calculate proportional efficacy accounting for the
            # proportion of people receiving a starter dose versus
            # completing a dose
            e_started = n_started * started_efficacy
            e_full = n_full * full_efficacy
            efficacy = (e_started + e_full) / (n_started + n_full)

            # Calculate herd immunity requirement
            herd_pct = (1 - (1 / r_0)) / efficacy

            if n_started + n_full >= population * herd_pct:
                days_to_herd_imm = day
                return date.today() + timedelta(days_to_herd_imm)
        raise ValueError("Herd immunity will take > 2 years.")