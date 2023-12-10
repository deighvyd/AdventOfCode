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
	}
}
