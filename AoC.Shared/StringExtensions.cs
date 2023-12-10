namespace AoC.Shared
{
	public static class StringExtensions
	{
		public static bool IsNullOrEmpty(this string value)
		{
			if (value == null)
			{
				return true;
			}

			if (value.Length == 0) 
			{
				return true;
			}

			return false;
		}
	}
}
