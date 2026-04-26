def print_profit_summary(dataframe, label):
    """Print a simple revenue, expense, and profit summary for a DataFrame."""
    total_revenue = dataframe["Revenue"].sum()
    total_expenses = dataframe["Expenses"].sum()
    total_profit = dataframe["Profit"].sum()

    

    print(f"\n{label} Summary:")
    print(f"Total revenue: {total_revenue:.2f}")
    print(f"Total expenses: {total_expenses:.2f}")
    print(f"Total profit: {total_profit:.2f}")


def create_financial_matrix(dataframe):
    """Create a matrix from Revenue, Expenses, and Profit columns."""
    matrix = dataframe[["Revenue", "Expenses", "Profit"]].to_numpy()

    print("\nFinancial matrix columns: Revenue, Expenses, Profit")
    print(matrix)

    return matrix
