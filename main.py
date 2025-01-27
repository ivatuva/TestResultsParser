import sys
from ingestion import FileReader
from parsing import Parser
from transformation.transformer import Transformer
from utils import setup_logging
from utils import handle_error
from utils.tech_enum import Tech
from database import MongoDBClient, DAO

def main():
    # Setup logging
    
    logger = setup_logging(__name__)

    # Validate and parse command line arguments
    if len(sys.argv) != 3:
        print("Usage: python main.py <file_path> <tech>")
        print(f"Supported techs: {', '.join(Tech.list())}")
        sys.exit(1)

    path = sys.argv[1]
    tech = sys.argv[2].lower()

    if tech not in Tech.list():
        print(f"Invalid tech. Supported techs: {', '.join(Tech.list())}")
        sys.exit(1)
    try:
        # Read the file
        file_reader = FileReader(path, tech)
        files_content = file_reader.read_file()
        logger.info("File read successfully.")
        
        # Parse the file content
        parser = Parser(logger)
        parsed_data = parser.parse(files_content, tech)
        logger.info("File parsed successfully.")

        # Transform the parsed data
        transformer = Transformer()
        transformed_data = transformer.transform(parsed_data, tech)
        logger.info("Data transformed successfully.")

        # Save the transformed data to MongoDB
        mongodb_client = MongoDBClient()
        dao = DAO(mongodb_client)
        dao.save(transformed_data.to_dict())
        logger.info("Data saved to MongoDB successfully.")
        
    except Exception as e:
        handle_error(e)
        logger.error("An error occurred: %s", e)
if __name__ == "__main__":
    main()
