namespace AoC.Shared
{
	public static class StringExtensions
	{
		public static bool IsNullOrWhitespace(this string value)
		{
			if (value == null)
			{
				return true;
			}

			if (value.Trim().Length == 0) 
			{
				return true;
			}

			return false;
		}

		public static List<int> ReadNumbers(this string value)
		{
			List<int> numbers = new List<int>();

			string[] numTokens = value.Trim().Split(' ');
			foreach (string token in numTokens) 
			{
				if (token.IsNullOrWhitespace())
				{
					continue;
				}

				numbers.Add(int.Parse(token.Trim()));
			}

			return numbers;
		}
	}
}
