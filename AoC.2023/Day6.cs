using System.Diagnostics;
using System.Runtime.CompilerServices;
using System.Text;

using AoC.Shared;

namespace AoC.Twenty23
{
	internal class Day6 : Day
	{
		public Day6() {}

		protected override uint DayNum => 6;

		protected override long GetTestResult(DayPart part)
		{
			switch (part)
			{
				case DayPart.One:
					return 288;
				case DayPart.Two:
					return 71503;
				default:
					throw new ArgumentException($"Unknown DayPart - {part}");
			}
		}

		private struct Race
		{
			public int Time;
			public int Distance;

			public Race(int time, int dist)
			{
				Time = time;
				Distance = dist;
			}
		}

		private List<Race> ReadRaces(string[] input)
		{
			List<Race> races = new();

			List<int> times = input[0].Split(':')[1].ReadNumbers<int>();
			List<int> distances = input[1].Split(':')[1].ReadNumbers<int>();

			for (int i = 0 ; i < times.Count ; ++i)
			{
				races.Add(new(times[i], distances[i]));
			}	

			return races;
		}

		protected override long SolvePartOne(string[] input)
		{
			List<Race> races = ReadRaces(input);

			List<int> solutions = new();
			foreach (Race race in races) 
			{
				int solutionCount = 0;
				for (int h = race.Time ; h >= 0 ; --h)
				{
					int dist = h * (race.Time - h);
					if (dist > race.Distance)
					{
						++solutionCount;
					}
				}

				solutions.Add(solutionCount);
			}

			return solutions.Aggregate(1, (x,y) => x * y);
		}

		protected override long SolvePartTwo(string[] input)
		{
			List<Race> races = ReadRaces(input);

			StringBuilder timeStr = new();
			StringBuilder distStr = new();
			foreach (Race race in races)
			{
				timeStr.Append(race.Time.ToString());
				distStr.Append(race.Distance.ToString());
			}

			long time = long.Parse(timeStr.ToString());
			long distance = long.Parse(distStr.ToString());
			
			int solutionCount = 0;
			for (long h = time ; h >= 0 ; --h)
			{
				long dist = h * (time - h);
				if (dist > distance)
				{
					++solutionCount;
				}
			}

            return solutionCount;
		}
	}
}
