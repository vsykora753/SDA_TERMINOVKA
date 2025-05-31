INSERT INTO users_user (
  last_login,
  is_superuser,
  email,
  password,
  role,
  first_name,
  last_name,
  birth_date,
  sex,
  organization_name,
  is_active,
  is_staff,
  website
)
VALUES
(
  '2025-05-13 20:00:00',
  1, -- is_superuser
  'marie.benešová0@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Marie',
  'Benešová',
  '2001-05-24',
  'M',
  'Běžecký spolek',
  1, -- is_active
  0, -- is_staff
  'https://www.zdravypohyb.cz'
),
(
  '2025-05-27 19:00:00',
  0, -- is_superuser
  'marie.procházka1@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Marie',
  'Procházka',
  '2010-12-19',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-23 20:00:00',
  1, -- is_superuser
  'petr.černý2@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Petr',
  'Černý',
  '2007-04-02',
  'F',
  'Běžecký spolek',
  1, -- is_active
  0, -- is_staff
  'https://www.maratonteam.cz'
),
(
  '2025-05-16 09:00:00',
  1, -- is_superuser
  'petr.svoboda3@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Petr',
  'Svoboda',
  '2012-03-15',
  'F',
  'Sportklub',
  1, -- is_active
  0, -- is_staff
  'https://www.runczech.cz'
),
(
  '2025-05-20 08:00:00',
  0, -- is_superuser
  'veronika.kučera4@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Veronika',
  'Kučera',
  '2015-05-18',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-20 09:00:00',
  1, -- is_superuser
  'jakub.kučera5@example.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Jakub',
  'Kučera',
  '2018-05-02',
  'F',
  'Běžecký spolek',
  1, -- is_active
  0, -- is_staff
  'https://www.runczech.cz'
),
(
  '2025-05-22 14:00:00',
  1, -- is_superuser
  'jakub.novák6@example.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Jakub',
  'Novák',
  '1997-08-27',
  'M',
  'Zdravý pohyb',
  1, -- is_active
  0, -- is_staff
  'https://www.zdravypohyb.cz'
),
(
  '2025-05-09 13:00:00',
  0, -- is_superuser
  'veronika.černý7@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Veronika',
  'Černý',
  '1998-07-19',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-14 12:00:00',
  1, -- is_superuser
  'tereza.horáková8@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Tereza',
  'Horáková',
  '2005-03-31',
  'F',
  'RunCzech',
  1, -- is_active
  0, -- is_staff
  'https://www.behejsnami.cz'
),
(
  '2025-05-10 16:00:00',
  1, -- is_superuser
  'jan.svoboda9@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Jan',
  'Svoboda',
  '1998-07-26',
  'F',
  'RunCzech',
  1, -- is_active
  0, -- is_staff
  'https://www.zdravypohyb.cz'
),
(
  '2025-05-12 13:00:00',
  1, -- is_superuser
  'eva.procházka10@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Eva',
  'Procházka',
  '2006-09-24',
  'F',
  'Běžecký spolek',
  1, -- is_active
  0, -- is_staff
  'https://www.runczech.cz'
),
(
  '2025-05-09 17:00:00',
  0, -- is_superuser
  'jan.král11@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Jan',
  'Král',
  '2012-12-13',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-10 12:00:00',
  0, -- is_superuser
  'martin.benešová12@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Martin',
  'Benešová',
  '2002-01-29',
  'F',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-05 13:00:00',
  0, -- is_superuser
  'martin.procházka13@example.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Martin',
  'Procházka',
  '2003-07-01',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-19 16:00:00',
  0, -- is_superuser
  'michal.veselý14@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Michal',
  'Veselý',
  '2006-11-26',
  'F',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-17 10:00:00',
  0, -- is_superuser
  'michal.horáková15@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Michal',
  'Horáková',
  '1998-02-19',
  'F',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-14 18:00:00',
  1, -- is_superuser
  'jakub.benešová16@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Jakub',
  'Benešová',
  '2012-09-29',
  'M',
  'Zdravý pohyb',
  1, -- is_active
  0, -- is_staff
  'https://www.behejsnami.cz'
),
(
  '2025-05-20 16:00:00',
  1, -- is_superuser
  'jan.černý17@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Jan',
  'Černý',
  '2011-11-02',
  'M',
  'Sportklub',
  1, -- is_active
  0, -- is_staff
  'https://www.maratonteam.cz'
),
(
  '2025-05-10 19:00:00',
  0, -- is_superuser
  'martin.dvořáková18@example.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Martin',
  'Dvořáková',
  '2001-06-10',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-19 11:00:00',
  1, -- is_superuser
  'petr.černý19@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Petr',
  'Černý',
  '1995-03-30',
  'F',
  'RunCzech',
  1, -- is_active
  0, -- is_staff
  'https://www.behejsnami.cz'
),
(
  '2025-05-01 20:00:00',
  0, -- is_superuser
  'martin.svoboda20@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Martin',
  'Svoboda',
  '1993-02-23',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-27 10:00:00',
  1, -- is_superuser
  'eva.král21@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Eva',
  'Král',
  '1988-06-07',
  'M',
  'Běžecký spolek',
  1, -- is_active
  0, -- is_staff
  'https://www.runczech.cz'
),
(
  '2025-05-11 08:00:00',
  0, -- is_superuser
  'eva.novák22@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Eva',
  'Novák',
  '2001-04-13',
  'F',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-16 08:00:00',
  1, -- is_superuser
  'tereza.kučera23@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Tereza',
  'Kučera',
  '1997-02-20',
  'F',
  'Sportklub',
  1, -- is_active
  0, -- is_staff
  'https://www.zdravypohyb.cz'
),
(
  '2025-05-01 08:00:00',
  1, -- is_superuser
  'eva.novák24@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Eva',
  'Novák',
  '2008-07-20',
  'F',
  'RunCzech',
  1, -- is_active
  0, -- is_staff
  'https://www.sportklub.cz'
),
(
  '2025-05-24 08:00:00',
  1, -- is_superuser
  'martin.benešová25@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Martin',
  'Benešová',
  '2007-08-03',
  'M',
  'Maraton tým',
  1, -- is_active
  0, -- is_staff
  'https://www.maratonteam.cz'
),
(
  '2025-05-09 09:00:00',
  1, -- is_superuser
  'eva.veselý26@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Eva',
  'Veselý',
  '1991-08-07',
  'F',
  'Běhej s námi',
  1, -- is_active
  0, -- is_staff
  'https://www.runczech.cz'
),
(
  '2025-05-16 17:00:00',
  1, -- is_superuser
  'lucie.benešová27@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Lucie',
  'Benešová',
  '2010-04-04',
  'M',
  'Běhej s námi',
  1, -- is_active
  0, -- is_staff
  'https://www.maratonteam.cz'
),
(
  '2025-05-20 18:00:00',
  1, -- is_superuser
  'tereza.veselý28@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Tereza',
  'Veselý',
  '1997-11-11',
  'M',
  'Sportklub',
  1, -- is_active
  0, -- is_staff
  'https://www.maratonteam.cz'
),
(
  '2025-05-12 08:00:00',
  1, -- is_superuser
  'michal.veselý29@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Michal',
  'Veselý',
  '2010-07-11',
  'F',
  'Maraton tým',
  1, -- is_active
  0, -- is_staff
  'https://www.zdravypohyb.cz'
),
(
  '2025-05-22 13:00:00',
  1, -- is_superuser
  'lucie.veselý30@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Lucie',
  'Veselý',
  '1996-08-25',
  'M',
  'RunCzech',
  1, -- is_active
  0, -- is_staff
  'https://www.behejsnami.cz'
),
(
  '2025-05-16 20:00:00',
  0, -- is_superuser
  'martin.kučera31@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Martin',
  'Kučera',
  '2012-07-24',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-11 19:00:00',
  0, -- is_superuser
  'petr.kučera32@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Petr',
  'Kučera',
  '2004-02-09',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-10 13:00:00',
  0, -- is_superuser
  'jan.procházka33@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Jan',
  'Procházka',
  '2005-11-19',
  'F',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-08 12:00:00',
  1, -- is_superuser
  'michal.novák34@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Michal',
  'Novák',
  '2001-09-14',
  'M',
  'Běhej s námi',
  1, -- is_active
  0, -- is_staff
  'https://www.runczech.cz'
),
(
  '2025-05-12 14:00:00',
  0, -- is_superuser
  'lucie.horáková35@example.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Lucie',
  'Horáková',
  '1998-12-23',
  'F',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-13 11:00:00',
  1, -- is_superuser
  'eva.veselý36@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Eva',
  'Veselý',
  '2018-09-12',
  'M',
  'Běžecký spolek',
  1, -- is_active
  0, -- is_staff
  'https://www.runczech.cz'
),
(
  '2025-05-14 13:00:00',
  1, -- is_superuser
  'petr.dvořáková37@example.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Petr',
  'Dvořáková',
  '2017-08-23',
  'M',
  'Běhej s námi',
  1, -- is_active
  0, -- is_staff
  'https://www.runczech.cz'
),
(
  '2025-05-22 13:00:00',
  1, -- is_superuser
  'petr.benešová38@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Petr',
  'Benešová',
  '1991-04-19',
  'M',
  'Zdravý pohyb',
  1, -- is_active
  0, -- is_staff
  'https://www.behejsnami.cz'
),
(
  '2025-05-19 09:00:00',
  1, -- is_superuser
  'tereza.kučera39@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Tereza',
  'Kučera',
  '1987-06-29',
  'F',
  'Běhej s námi',
  1, -- is_active
  0, -- is_staff
  'https://www.sportklub.cz'
),
(
  '2025-05-06 10:00:00',
  0, -- is_superuser
  'petr.procházka40@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Petr',
  'Procházka',
  '2001-06-18',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-09 20:00:00',
  0, -- is_superuser
  'michal.kučera41@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Michal',
  'Kučera',
  '2014-11-26',
  'F',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-09 11:00:00',
  1, -- is_superuser
  'lucie.horáková42@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Lucie',
  'Horáková',
  '2002-10-06',
  'F',
  'Sportklub',
  1, -- is_active
  0, -- is_staff
  'https://www.runczech.cz'
),
(
  '2025-05-28 09:00:00',
  1, -- is_superuser
  'lucie.dvořáková43@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Lucie',
  'Dvořáková',
  '1987-02-23',
  'F',
  'Zdravý pohyb',
  1, -- is_active
  0, -- is_staff
  'https://www.maratonteam.cz'
),
(
  '2025-05-01 13:00:00',
  1, -- is_superuser
  'jan.procházka44@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Jan',
  'Procházka',
  '2001-07-07',
  'F',
  'Zdravý pohyb',
  1, -- is_active
  0, -- is_staff
  'https://www.zdravypohyb.cz'
),
(
  '2025-05-17 16:00:00',
  0, -- is_superuser
  'marie.veselý45@example.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Marie',
  'Veselý',
  '1998-10-26',
  'F',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-13 13:00:00',
  0, -- is_superuser
  'petr.novák46@seznam.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Petr',
  'Novák',
  '1997-08-19',
  'F',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-05 17:00:00',
  0, -- is_superuser
  'lucie.novák47@mail.cz',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'R',
  'Lucie',
  'Novák',
  '2010-09-17',
  'M',
  '',
  1, -- is_active
  0, -- is_staff
  ''
),
(
  '2025-05-27 20:00:00',
  1, -- is_superuser
  'michal.horáková48@gmail.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Michal',
  'Horáková',
  '2000-05-15',
  'M',
  'RunCzech',
  1, -- is_active
  0, -- is_staff
  'https://www.runczech.cz'
),
(
  '2025-05-07 15:00:00',
  1, -- is_superuser
  'michal.veselý49@example.com',
  'pbkdf2_sha256$260000$fake$hashvaluehere',
  'O',
  'Michal',
  'Veselý',
  '2012-02-24',
  'F',
  'Zdravý pohyb',
  1, -- is_active
  0, -- is_staff
  'https://www.behejsnami.cz'
);