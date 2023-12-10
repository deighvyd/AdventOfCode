using System.Runtime.CompilerServices;
using System.Text;
using System.Linq;

using AoC.Shared;

namespace AoC.Twenty23
{
	internal class Day3 : Day
	{
		public Day3() {}

		protected override uint DayNum => 3;

		protected override int GetTestResult(DayPart part)
		{
			switch (part)
			{
				case DayPart.One:
					return 4361;
				case DayPart.Two:
					return 467835;
				default:
					throw new ArgumentException($"Unknown DayPart - {part}");
			}
		}

		private struct Coord
		{
			public int X;
			public int Y;

			public Coord(int x, int y)
			{
				X = x; 
				Y = y;
			}
		}

		private struct Part
		{
			public int Num;
			public int Length;
			public Coord Loc;

			public Part(int num, int len, Coord loc)
			{
				Num = num;
				Length = len;
				Loc = loc;
			}

			public bool IsAdjacent(Symbol sym)
			{
				if (Loc.Y > (sym.Loc.Y + 1) || Loc.Y < (sym.Loc.Y - 1))
				{
					return false;
				}

				if ((Loc.X + Length) < sym.Loc.X || Loc.X > (sym.Loc.X + 1))
				{
					return false;
				}

				return true;
			}
		}

		private struct Symbol
		{
			public char Type;
			public Coord Loc;

			public Symbol(char type, Coord loc)
			{
				Type = type;
				Loc = loc;
			}
		}

		private (List<Part>, List<Symbol>) ReadSchematic(string[] input)
		{
			int y = 0;
			List<Part> parts = new();
			List<Symbol> symbols = new();

			foreach (string line in input)
			{
				for (int x = 0 ; x < line.Length ; ++x)
				{
					char c = line[x];

					if (char.IsDigit(c)) 
					{
						Coord loc = new Coord(x, y);

						StringBuilder numStr = new();
						while (x < line.Length && char.IsDigit(line[x]))
						{
							numStr.Append(line[x]);
							++x;
						}
						--x;

						int num = int.Parse(numStr.ToString());
						parts.Add(new(num, numStr.Length, loc));
					}
					else if (c != '.')
					{
						 symbols.Add(new(c, new(x, y)));
					}
				}	

				++y;
			}

			return (parts, symbols);
		}

		protected override int SolvePartOne(string[] input)
		{
			(List<Part> parts, List<Symbol> symbols) = ReadSchematic(input);

			int total = 0;
			foreach (Part part in parts) 
			{
				foreach (Symbol sym in symbols)
				{
					if (part.IsAdjacent(sym))
					{
						total += part.Num;
						break;
					}
				}
			}

			return total;
		}

		protected override int SolvePartTwo(string[] input)
		{
			(List<Part> parts, List<Symbol> symbols) = ReadSchematic(input);

			int total = 0;
			foreach (Symbol sym in symbols)
			{
				if (sym.Type != '*')
				{
					continue;
				}

				List<Part> adjParts = parts.Where(x => x.IsAdjacent(sym)).ToList();
				if (adjParts.Count == 2)
				{
					int ratio = adjParts[0].Num * adjParts[1].Num;
					total += ratio;

				}
			}

			return total;
		}
	}
}
