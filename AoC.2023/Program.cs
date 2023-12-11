using AoC.Shared;

namespace AoC.Twenty23
{
	internal class Program : AdventOfCode
	{
		Program()
		{
			CurrentDay = 1;
		}

		static void Main(string[] args)
		{
			Day day = new Day6();
			day.Solve(DayPart.One);
			day.Solve(DayPart.Two);
		}
	}
}
