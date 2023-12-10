namespace AoC.Shared
{
	public abstract class Day : IDay
	{
		protected Day() { }

		protected abstract uint DayNum { get; }

		protected abstract long GetTestResult(DayPart part);

		private string[] ReadInput(DayPart part, bool test)
		{
			string ext = test ? "test" : "input";
			string filename = $"data\\day{DayNum}.{part.ToDigitString()}.{ext}";
			return File.ReadAllLines(filename);
		}

		public void Solve(DayPart part)
		{
			long testResult = Solve(part, true);
			Console.WriteLine($"Day {DayNum}.{part.ToDigitString()} Test Result = {testResult} Expected Result = {GetTestResult(part)}");
			if (testResult == GetTestResult(part))
			{
				long result = Solve(part, false);
				Console.WriteLine($"Day {DayNum}.{part.ToDigitString()} Result = {result}");
			}
		}

		private long Solve(DayPart part, bool test)
		{
			switch (part)
			{
				case DayPart.One:
					return SolvePartOne(ReadInput(part, test));
				case DayPart.Two:
					return SolvePartTwo(ReadInput(part, test));
				default:
					throw new ArgumentException($"Unknown DayPart - {part}");
			}
		}

		protected abstract long SolvePartOne(string[] input);
		protected abstract long SolvePartTwo(string[] input);
	}
}
