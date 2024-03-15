# Birthpoet

'Birthpoet' writes three verses of lyrical poetry about the birth date and birth location of a person. 'Birthpoet' uses an OpenAI Assistant, which calls a function that connects to NOAA's climate data daily summaries and returns some basic information about the weather on the submitted date. The Assistant then uses that information, along with the context of the location and a new birth, to write a celebratory birthday poem.

## Features

- A ready-made OpenAI API Assistant instructed to create short relevant poems about a named individual and the environment at the location on the date of their birth.
- 'Function calling' tool activated with the Assistant, allowing it to call a 'get_weather_details' tool.
- A function triggered by activating the 'get_weather_details' tool. The function determines the weather station with relevant information which is nearest to the birth location and recorded information for the birth date. The function acquires the information then formats it and returns it to the Assistant for use in the poem's construction.

## Getting Started

'Birthpoet' was created to compose beautiful poems about a person's day of birth. Follow the instructions below to set up and start using 'Birthpoet'.

### Prerequisites

Before you begin, you will need the following requirements:

- **Python 3.8+**: The project is written in Python and requires Python 3.8 or newer. [Download Python](https://www.python.org/downloads/).
- **pip**: Used for installing dependencies. Comes installed with Python 3.4 and above.
- **An OpenAI API key**: Required to access OpenAI's services. Obtain one from [OpenAI](https://openai.com/api/).
- **A NOAA weather web services token: Required for the tool to access weather data. Obtain one from [NOAA](https://www.ncdc.noaa.gov/cdo-web/token)

### Installation

1. **Clone the repository**:

```bash
git clone https://github.com/PaulArthurMiller/birthpoet.git
cd birthpoet
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a .env file in the root directory and add your OpenAI API key:

```python
OPENAI_API_KEY='your_api_key_here'
NOAA_KEY_TOKEN='your_NOAA_token_here'
```

4. **Run the application (if applicable)**:
```bash
python birthpoet_assistant.py
```

### Usage

This project can be run as currently configured to produce poems about a person's birth date environment. However, potential issues may arise depending on the availability of weather data from nearby sites on the date requested. In the tool at line 95, in the 'calculate_bounding_box' function, the 'distance' parameter may be expanded to draw in more weather stations and their accompanying data. However, NOAA's Climate Data Online defaults to 25 stations in the search, which can cut off closer stations with better data in some situations. This may be an area for further development of the Assistant/tool interface.

To start the assistant, run:

```bash
python birthpoet_assistant.py
```

**Generating a Poem**
To generate a poem, follow the prompts after starting the application. Example:

'Let's make a great birthday message! Would you please tell me the name of the person we're celebrating, their birthdate, and their birth location?'

Respond with the name, birthdate, and location. The assistant will generate a personalized poem based on the weather conditions of the birthdate and location provided.

**Updating the Assistant**
The script to update the Assistant's configuration is not included in the public repository for security reasons.

For more detailed documentation, visit [OpenAI Documentation](https://platform.openai.com/docs/assistants/overview?context=with-streaming).

## License

This repository is under the NN license.

## Contact Information

This project was created by Paul Miller. He can be reached at PaulArthurMiller@Gmail.com.