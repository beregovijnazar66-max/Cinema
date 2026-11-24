from collections import deque


class Visitor:
    def __init__(self, name):
        self.name = name
        self.checked_in = False   # пройшов контроль квитків
        self.seated = False       # сів на своє місце

    def check_in(self):
        self.checked_in = True

    def take_seat(self):
        if self.checked_in:
            self.seated = True
        else:
            print(f"{self.name} не пройшов контроль квитків")


class Ticket:
    def __init__(self, number, visitor, session_id, seat):
        self.number = number
        self.visitor = visitor
        self.session_id = session_id
        self.seat = seat

    def show_info(self):
        print(
            f"Квиток №{self.number}, "
            f"глядач: {self.visitor.name}, "
            f"сеанс: {self.session_id}, "
            f"місце: {self.seat}"
        )


class Session:
    def __init__(self, session_id, film, delay=0):
        self.session_id = session_id
        self.film = film
        self.delay = delay
        self.status = "очікується"
        self.tickets = []
        self.hall = None

    def add_ticket(self, ticket):
        if ticket.session_id != self.session_id:
            print("Квиток належить іншому сеансу")
            return

        self.tickets.append(ticket)

    def count_visitors(self):
        return len(self.tickets)

    def count_checked_in(self):
        return sum(1 for t in self.tickets if t.visitor.checked_in)

    def count_seated(self):
        return sum(1 for t in self.tickets if t.visitor.seated)

    def check_in_visitors(self):
        self.status = "контроль квитків"

        print(
            f"Сеанс {self.session_id}: "
            f"пройшли контроль {self.count_checked_in()} "
            f"з {self.count_visitors()} глядачів"
        )

    def seat_visitors(self):
        self.status = "розсадка"

        print(
            f"Сеанс {self.session_id}: "
            f"у залі розмістилися {self.count_seated()} глядачів"
        )

        missed = self.count_checked_in() - self.count_seated()
        print(f"Не зайняли місця: {missed} глядачів")

    def delay_session(self):
        if self.delay > 0:
            print(
                f"Сеанс {self.session_id} "
                f"затримується на {self.delay} хвилин"
            )
        else:
            print(
                f"Сеанс {self.session_id} "
                f"починається без затримки"
            )

    def change_status(self, new_status):
        self.status = new_status

    def show_info(self):
        print(
            f"Сеанс {self.session_id}: "
            f"«{self.film}», "
            f"глядачів: {self.count_visitors()}, "
            f"пройшли контроль: {self.count_checked_in()}, "
            f"сіли: {self.count_seated()}, "
            f"статус: {self.status}"
        )


class Hall:
    def __init__(self, number):
        self.number = number
        self.available = True
        self.total_sessions = 0

    def start_session(self, session):
        if not self.available:
            print(f"Зал №{self.number} зайнятий")
            return False

        self.available = False

        print(f"\nЗал №{self.number} зайнятий")
        print(f"Сеанс {session.session_id} готується до початку")

        session.hall = self.number
        session.change_status("показано")

        print(
            f"Фільм «{session.film}» успішно показано "
            f"в залі №{self.number}!"
        )

        self.total_sessions += 1
        self.available = True

        return True


class Cinema:
    def __init__(self):
        self.sessions = deque()
        self.halls = [Hall(1), Hall(2)]
        self.finished_sessions = []

        self.total_sessions = 0
        self.total_visitors = 0
        self.total_checked_in = 0
        self.total_seated = 0

        self.delayed_sessions = 0
        self.total_delay = 0

    def add_session(self, session):
        self.sessions.append(session)

    def show_sessions(self):
        print("\n========== СЕАНСИ В КІНОТЕАТРІ ==========")

        if not self.sessions:
            print("Сеансів немає")
            return

        for session in self.sessions:
            session.show_info()

    def process_next_session(self, hall):
        if not self.sessions:
            print("\nВ кінотеатрі немає сеансів")
            return

        if not hall.available:
            print("\nЗал зайнятий")
            return

        session = self.sessions.popleft()

        print("\n====================================")
        print(f"ОБСЛУГОВУВАННЯ СЕАНСУ {session.session_id}")
        print(f"Фільм: {session.film}")
        print("====================================")

        session.check_in_visitors()
        session.seat_visitors()
        session.delay_session()

        session.change_status("готовий до початку")

        if hall.start_session(session):
            self.finished_sessions.append(session)

            self.total_sessions += 1
            self.total_visitors += session.count_visitors()
            self.total_checked_in += session.count_checked_in()
            self.total_seated += session.count_seated()

            if session.delay > 0:
                self.delayed_sessions += 1
                self.total_delay += session.delay
        else:
            self.sessions.appendleft(session)

    def process_all_sessions(self):
        hall_index = 0

        while self.sessions:
            hall = self.halls[hall_index]

            self.process_next_session(hall)

            hall_index = (hall_index + 1) % len(self.halls)

    def show_statistics(self):
        missed = self.total_checked_in - self.total_seated
        not_checked_in = self.total_visitors - self.total_checked_in

        print("\n========== СТАТИСТИКА КІНОТЕАТРУ ==========")

        print(f"Успішно проведено сеансів: {self.total_sessions}")
        print(f"Всього глядачів: {self.total_visitors}")
        print(f"Пройшли контроль квитків: {self.total_checked_in}")
        print(f"Не пройшли контроль: {not_checked_in}")
        print(f"Сіли на місця: {self.total_seated}")
        print(f"Не сіли на місця: {missed}")

        print(f"Затримано сеансів: {self.delayed_sessions}")
        print(f"Загальний час затримок: {self.total_delay} хв")

        print("\nСТАТИСТИКА ЗАЛІВ:")

        for hall in self.halls:
            print(
                f"Зал №{hall.number}: "
                f"{hall.total_sessions} сеанси"
            )

        print("\nСТАТУСИ ВСІХ СЕАНСІВ:")

        for session in self.finished_sessions:
            print(
                f"Сеанс {session.session_id}: "
                f"{session.status}, "
                f"зал №{session.hall}"
            )

        print("=========================================")


session1 = Session("S101", "Дюна", 15)
session2 = Session("S202", "Інтерстеллар", 0)
session3 = Session("S303", "Матриця", 0)
session4 = Session("S404", "Месники", 40)
# (сеанс, всього квитків, пройшли контроль, сіли на місця)
sessions_data = [
    (session1, 130, 125, 120),
    (session2, 150, 148, 145),
    (session3, 100, 96, 93),
    (session4, 200, 194, 191),
]

for session, total, checked_in, seated in sessions_data:
    for i in range(1, total + 1):
        visitor = Visitor(f"Глядач {session.session_id}-{i}")

        ticket = Ticket(
            f"{session.session_id}-{i}",
            visitor,
            session.session_id,
            i,
        )

        if i <= checked_in:
            visitor.check_in()

        if i <= seated:
            visitor.take_seat()

        session.add_ticket(ticket)

cinema = Cinema()

cinema.add_session(session1)
cinema.add_session(session2)
cinema.add_session(session3)
cinema.add_session(session4)

cinema.show_sessions()

cinema.process_all_sessions()

print("\n========== СЕАНСИ, ЯКІ ЗАЛИШИЛИСЯ ==========")

if not cinema.sessions:
    print("Усі сеанси успішно проведені!")
else:
    cinema.show_sessions()

cinema.show_statistics()
