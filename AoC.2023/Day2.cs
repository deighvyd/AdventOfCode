using System.Runtime.CompilerServices;
using System.Text;

using AoC.Shared;

namespace AoC.Twenty23
{
	internal class Day2 : Day
	{
		public Day2() {}

		protected override uint DayNum => 2;

		protected override int GetTestResult(DayPart part)
		{
			switch (part)
			{
				case DayPart.One:
					return 8;
				case DayPart.Two:
					return 2286;
				default:
					throw new ArgumentException($"Unknown DayPart - {part}");
			}
		}

		struct Bag
		{
			public uint Red;
			public uint Green;
			public uint Blue;

			public Bag()
			{
			}

			public Bag(uint red, uint green, uint blue)
			{
				Red = red;
				Green = green;
				Blue = blue;
			}
		}

		protected override int SolvePartOne(string[] input)
		{
			Bag bag = new(12, 13, 14);

			int id = 0;
			int total = 0;
			foreach (string line in input)
			{
				if (line.IsNullOrWhitespace())
				{
					continue;
				}	

				++id;

				bool possible = true;
				string[] gameTokens = line.Split(':');
				string[] drawTokens = gameTokens[1].Split(';');
				foreach (string draw in drawTokens)
				{
					string[] colourTokens = draw.Trim().Split(',');
					foreach (string colour in colourTokens)
					{
						string[] tokens = colour.Trim().Split(' ');
						int count = int.Parse(tokens[0].Trim());
						switch (tokens[1])
						{
							case "red":
								if (count > bag.Red) 
								{
									possible = false;
								}
								break;

							case "green":
								if (count > bag.Green) 
								{
									possible = false;
								}
								break;

							case "blue":
								if (count > bag.Blue) 
								{
									possible = false;
								}
								break;
						}
					}

					if (!possible)
					{
						break;
                    }
				}

				if (possible)
				{
					total += id;
				}
			}

			return total;
		}

		protected override int SolvePartTwo(string[] input)
		{
			int total = 0;
			foreach (string line in input)
			{
				if (line.IsNullOrWhitespace())
				{
					continue;
				}	

				Bag bag = new Bag();

				string[] gameTokens = line.Split(':');
				string[] drawTokens = gameTokens[1].Split(';');
				foreach (string draw in drawTokens)
				{
					string[] colourTokens = draw.Trim().Split(',');
					foreach (string colour in colourTokens)
					{
						string[] tokens = colour.Trim().Split(' ');
						uint count = uint.Parse(tokens[0].Trim());
						switch (tokens[1])
						{
							case "red":
								bag.Red = uint.Max(bag.Red, count);
								break;

							case "green":
								bag.Green = uint.Max(bag.Green, count);
								break;

							case "blue":
								bag.Blue = uint.Max(bag.Blue, count);
								break;
						}
					}
				}

				uint num = (bag.Red * bag.Green * bag.Blue);
				total += (int)num;
			}

			return total;
		}
	}
}
