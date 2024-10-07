# ModernAttire

## Table of Contents

- [ModernAttire](#modernattire)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Entity-Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Makefile Usage](#makefile-usage)
  - [License](#license)



## Project Overview

This project is an online clothing store and a practical web development exercise.


## Entity-Relationship Diagram (ERD)

You can view the ERD in draw.io by following the link below:

[View ERD in draw.io](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&target=blank&highlight=0000ff&layers=1&nav=1&title=ModernAttire.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1OmqKRK3yz30yio26DFVY6PWpaAafJrdm%26export%3Ddownload)




## Features

- **User Registration**: Users can register using only their phone number, which must be verified for account activation.
- **User Login**: Users can log in using their phone number and password or their email address and password.
- **Simple User Profile**: Each user has a straightforward profile to manage their personal information.




## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Docker
- Docker Compose
- Make


### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/REZASH600/ModernAttire.git
   ```

2. **Go to the project directory:**
   ‍‍‍‍
   ```bash
   cd ModernAttire
   ```

3. **Build the Docker images:**
   ```bash
   make l-build
   ```

### Makefile Usage

The Makefile contains various commands to simplify your workflow. Here are some of the key commands and their descriptions:

- **`make l-build`**: Builds the Docker images and starts the services in detached mode.
  
- **`make l-up`**: Starts the services defined in the Docker Compose file.
  
- **`make l-stop`**: Stops the running services without removing them.
  
- **`make l-down`**: Stops and removes all services and associated containers.
  
- **`make l-logs`**: Displays the logs for all running services.
  
- **`make l-status`**: Shows the status of all running containers.
  
For a complete list of commands and their descriptions, you can refer to the [Makefile](./Makefile).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



