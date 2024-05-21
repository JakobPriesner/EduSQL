
# Lern-SQL Project

## Overview

This project is a study initiative developed by students at Technische Hochschule Würzburg Schweinfurt. The main objective was to learn the usage of databases, particularly focusing on complex SQL operations and working with multiple parallel DB operations. A Postgresql database was set up and used for this project.

## Project Structure

The project is divided into two main parts:
1. **Backend**: Contains the server-side code and the database schema.
2. **Frontend**: Contains the client-side code.

## Dataset

Within the `.gitignored` data folder, there is a dataset provided by the university, which includes some internal data. The detailed list of provided data files is as follows:

- **address.csv**: street, house_number, address_addition, city, country, postal_code
- **lecturer.csv**: id, firstname, lastname, address, roomnumber, phone, title, email, lastmodified, homepagehref, homepagemediatype, homepagerelationtype, mobile, type, cn, gender
- **location.csv**: area, lectureroomcount, building_count, mensa, parking_slots, library, street, house_number, address_addition, city, country, postal_code
- **moduledescription.csv**
- **permission.csv**: alias, description
- **person.csv**: first_name, last_name, title_id, date_of_birth, email, k_number, password_hash, salt, session_token
- **room.csv**: id, totalnumberofseats, maxnumberofseatsforexam3rdrowempty, campus, numberofseatswithcomputer, numberofseatsperrow, maxnumberofseatsforexam2ndrowempty, maxnumberofseatsforexam, canbeusedforexam, name, belongstofhws, location0, location1, comment, maphref, mapmediatype, maprelationtype, totalnumberofrows, lastmodified, nameoflab, labroom, canbeusedforclass, faculty, usedas, spaceinsqm, numberofseatscorona
- **sre_attachment.csv**: id, name, validfrom, validto, lastmodified, spoimagebinary, spoimage
- **sre_to_attachment.csv**: leftid, rightid
- **sre.csv**: id, legallyvalidsince, pdffile, name, studyprogram, lastmodified, city, streetname, housenumber
- **staff.csv**: staff_type, salary, temporary_to, employed_since, hours_per_week, holidays, social_security_id, iban, released, paused
- **student.csv**: matriculation_number, etc_score, in_student_council, enrolled_at, exmatriculated_at
- **vacation.csv**: justification, approved, semester_count
- **vl_plan.csv**: Datum, Beginn, Ende, Art, Veranstaltung, Dozent, Raum, Untergruppe, Studiengruppe, Anmerkung, V.-Nummer 1

## Development Process

### Data Transformation

The first step was to use the provided data and transform it into our data structure, visualized in `docs/erm/`. Missing data were generated as needed.

### Website and API Development

Once the data transformation was complete, a website with an API was developed to help students learn SQL. The website tells the story of a person enrolling in a study program at THWS, completing their studies, working as a scientific assistant, and eventually becoming a professor. The person has to update their data within the database throughout this process, such as enrolling themselves, adding written exams, etc. Each step is verified, allowing students to use different SQL approaches to achieve the correct results. Hints are provided if students get stuck.

### Learning Objective

The website aims to help students learn SQL by using a realistic and familiar dataset from the university itself. 

## Performance Challenges

Due to the nature of the project, several performance challenges were encountered:

- **Parallel Database Operations**: Handling multiple concurrent operations on the database led to significant performance bottlenecks.
- **Complex Calculations**: Performing complex calculations within SQL queries slowed down the system, especially with larger datasets.
- **Data Transformation**: The initial transformation of the provided data into the project's data structure was resource-intensive.
- **API Response Time**: Ensuring that the API responses were timely while processing extensive SQL operations was a challenge.

## Important Notes

- This project is a study project and should not be used in production or made publicly accessible.
- Authentication and security were not the focus due to time constraints and the educational nature of the project.
- The development time for the API and UI was limited to one week.

## Project Setup

### Prerequisites

- PostgreSQL
- Node.js
- Python

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lern-sql.git
   cd lern-sql
   ```

2. Start the docker-container
   ```bash
   docker compose up
   ```

### Usage

Access the website at `http://localhost:4200` and follow the guided steps to learn SQL using the provided dataset.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
