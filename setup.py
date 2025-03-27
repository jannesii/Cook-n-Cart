from setuptools import setup

setup(
    name="Cook-n-Cart",
    version="0.1.0",
    description="Cook-n-Cart application",
    author="Your Name",
    author_email="your.email@example.com",
    # List the modules that are directly in your root directory
    py_modules=[
        "main",
        "root_controllers",
        "root_database",
        "root_models",
        "root_repositories",
        "views_asetukset_page",
        "views_main_window",
        "views_ostoslistat_page",
        "views_reseptit_page",
        "views_tuotteet_page",
        "widgets_add_products_widget",
        "widgets_add_recipe_widget",
        "widgets_add_shoplist_widget",
        "widgets_add_tags_widget",
        "widgets_conversion_service",
        "widgets_edit_product_widget",
        "widgets_edit_recipe_widget",
        "widgets_import_recipe_widget",
        "widgets_product_detail_widget",
        "widgets_recipe_detail_widget",
        "widgets_shoplist_detail_widget",
    ],
    install_requires=[
        "PySide6>=6.8.0",
    ],
    package_data={
        # Include any non-Python files needed by the application
        "": [
            "cookncart/resources/images/*",
            "utils/config.json",
            "utils/cook_and_cart.db",
        ],
    },
    entry_points={
        "console_scripts": [
            "cookncart = main:main",  # Ensure main.py has a main() function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
