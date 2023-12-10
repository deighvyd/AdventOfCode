namespace AoC.Shared
{
	public enum DayPart
	{
		One,
		Two
	};

	public static class DayPartExtenstions
	{
		public static string ToDigitString(this DayPart part)
        {
			switch (part)
			{
				case DayPart.One:
					return "1";
				case DayPart.Two:
					return "2";
				default:
					throw new ArgumentException($"Unknown DayPart - {part}");
			}
        }
	}
}
