using System.Runtime.CompilerServices;
using System.Text;

using AoC.Shared;

namespace AoC.Twenty23
{
	internal class Day1 : Day
	{
		public Day1() {}

		protected override uint DayNum => 1;

		protected override int GetTestResult(DayPart part)
		{
			switch (part)
			{
				case DayPart.One:
					return 142;
				case DayPart.Two:
					return 281;
				default:
					throw new ArgumentException($"Unknown DayPart - {part}");
			}
		}

		protected override int SolvePartOne(string[] input)
		{
			int total = 0;
			foreach (string line in input)
			{
				StringBuilder numStr = new();
				numStr.Append(line.First(x => char.IsDigit(x)));
				numStr.Append(line.Last(x => char.IsDigit(x)));

				int num = int.Parse(numStr.ToString());
				total += num;
			}

			return total;
		}

		private static readonly string[] EnglishNumbers = { "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};

		private int GetFirstNum(string s)
		{
			for (int i = 0 ; i < s.Length ; ++i)
			{
				if (char.IsDigit(s[i]))
				{
					return int.Parse(s[i].ToString());
				}
				else
				{
					for (int j = 0 ; j < EnglishNumbers.Length ; ++j) 
					{
						if (s.IndexOf(EnglishNumbers[j]) == i)
						{
							return j + 1;
						}
					}
				}
			}

			return 0;
		}

		private int GetSecondNum(string s)
		{
			if (s.IsNullOrWhitespace())
			{
				return 0;
			}

			for (int i = s.Length ; i > 0 ; --i)
			{
				int idx = i - 1;
				if (char.IsDigit(s[idx]))
				{
					return int.Parse(s[idx].ToString());
				}
				else
				{
					for (int j = 0 ; j < EnglishNumbers.Length ; ++j) 
					{
						if (s.LastIndexOf(EnglishNumbers[j]) == idx)
						{
							return j + 1;
						}
					}
				}
			}

			return 0;
		}

		protected override int SolvePartTwo(string[] input)
		{
			int total = 0;
			foreach (string line in input)
			{
				int firstNum = GetFirstNum(line);
				int secondNum = GetSecondNum(line);	
				int num = (firstNum * 10) + secondNum;
				total += num;
			}

            return total;
		}
	}
}
