using System.Net.Mail;
using System.Runtime.CompilerServices;
using System.Text;

using AoC.Shared;

namespace AoC.Twenty23
{
	internal class Day5 : Day
	{
		public Day5() {}

		protected override uint DayNum => 5;

		protected override long GetTestResult(DayPart part)
		{
			switch (part)
			{
				case DayPart.One:
					return 35;
				case DayPart.Two:
					return -1;
				default:
					throw new ArgumentException($"Unknown DayPart - {part}");
			}
		}

		private struct Range
		{
			public ulong SourceStart;
			public ulong SourceEnd => SourceStart + Length;
			public ulong DestStart;
			public ulong DestEnd => DestStart + Length;
			public ulong Length;

			public Range(string range)
			{
				List<ulong> rangeElems = range.ReadNumbers<ulong>();
				SourceStart = rangeElems[1];
				DestStart = rangeElems[0];
				Length = rangeElems[2];
			}
		}

		protected override long SolvePartOne(string[] input)
		{
			List<ulong> seedList = input[0].Split(':')[1].ReadNumbers<ulong>();

			List<List<Range>> maps = new();
			for (int i = 1 ; i < input.Length ; ++i)
			{
				string line = input[i];
				if (line.IsNullOrWhitespace())
				{
					continue;
				}

				if (!char.IsDigit(line[0]))
				{
					maps.Add(new());
				}
				else
				{
					maps.Last().Add(new(line));
				}
			}
			
			ulong bestLoc = int.MaxValue;
			foreach (ulong seed in seedList)
			{
				ulong lookup = seed;
				foreach (List<Range> map in maps)
				{
					ulong result = 0;
					bool mapped = false;
					foreach (Range range in map)
					{
						if (lookup >= range.SourceStart && lookup < range.SourceEnd)
						{
							result = range.DestStart + (lookup - range.SourceStart);
							mapped = true;
							break;
						}
					}

					if (!mapped)
					{
						result = lookup;
					}
					lookup = result;
				}

				bestLoc = ulong.Min(bestLoc, lookup);
			}

			return (long)bestLoc;
		}

		protected override long SolvePartTwo(string[] input)
		{
            return 0;
		}
	}
}
