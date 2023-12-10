using System.Numerics;

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

		public static List<T> ReadNumbers<T>(this string value) where T : IBinaryInteger<T>
		{
			List<T> numbers = new List<T>();

			string[] numTokens = value.Trim().Split(' ');
			foreach (string token in numTokens) 
			{
				if (token.IsNullOrWhitespace())
				{
					continue;
				}

				numbers.Add(T.Parse(token.Trim(), System.Globalization.NumberStyles.Integer, null));
			}

			return numbers;
		}
	}
}
