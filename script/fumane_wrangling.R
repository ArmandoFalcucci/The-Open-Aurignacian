# Load necessary libraries
library(dplyr)

# Define paths for both datasets
threeD_path <- "data/RF_volume_area.csv"
dataset_path <- "data/RF_dataset_blank.csv"
cores_dataset_path <- "data/RF_dataset_core.csv"
scanner_path <- "data/RF_3D_Dataset_List.csv"

# Read the main dataset and the cores dataset
threeDdataset <- read.csv(threeD_path)
dataset <- read.csv(dataset_path)
cores_dataset <- read.csv(cores_dataset_path)
scanner_dataset <- read.csv(scanner_path)


# Perform the join with only the 'Scanner' column from scanner_dataset
merged_data <- threeDdataset %>%
  left_join(scanner_dataset %>% select(ID, Scanner, Unit, Raw.material, Length, Width, Thickness), by = "ID")

# Check for any rows where 'Scanner' is NA
merged_data %>%
  filter(is.na(Scanner))

# Load the necessary library
library(dplyr)

# Select the required columns from the dataset
dataset_selected <- dataset %>%
  select(ID, class, blank, technology, cortex, preservation)

# Merge with threeDdataset using the 'ID' column
merged_data <- merged_data %>%
  left_join(dataset_selected, by = "ID") %>%
  mutate(Site = "Fumane") %>%
  select(-mesh)


# Select the 'Core.classification' column from the cores dataset and rename it to 'Core_classification'
cores_classification <- cores_dataset %>%
  select(ID, classification.1) %>%
  rename(Core_classification = classification.1)

# Join the two datasets on the 'ID' column
final_dataset <- merged_data %>%
  left_join(cores_classification, by = "ID")


# Load the necessary library
library(dplyr)

# Replace NA values with custom words in specific columns
final_dataset <- final_dataset %>%
  mutate(
    class = if_else(is.na(class), "Core", class),
    blank = if_else(is.na(blank), "Other", blank),
    technology = if_else(is.na(technology), "Other", technology),
    preservation = if_else(is.na(preservation), "Other", preservation)
  )

cortex_cores <- cores_dataset %>%
  select(ID, cortex) %>%
  rename(Cortex = cortex)

# Perform the join with only the 'Scanner' column from scanner_dataset
final_dataset <- final_dataset %>%
  left_join(cortex_cores, by = "ID")



# Save the final dataset to a new CSV file
write.csv(final_dataset, "data/FUMANE.csv", row.names = FALSE)
