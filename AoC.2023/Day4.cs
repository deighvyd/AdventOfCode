using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Text;

using AoC.Shared;

namespace AoC.Twenty23
{
	internal class Day4 : Day
	{
		public Day4() {}

		protected override uint DayNum => 4;

		protected override int GetTestResult(DayPart part)
		{
			switch (part)
			{
				case DayPart.One:
					return 13;
				case DayPart.Two:
					return 30;
				default:
					throw new ArgumentException($"Unknown DayPart - {part}");
			}
		}

		private struct Card
		{
			public List<int> WinningNumbers;
			public List<int> HaveNumbers;
		}

		private List<Card> ReadCards(string[] input)
		{
			List<Card> cards = new List<Card>();

			foreach (string line in input)
			{
				string[] gameTokens = line.Split(':');
				string[] numberTokens = gameTokens[1].Split('|');

				List<int> winningNumbers = numberTokens[0].ReadNumbers();
				List<int> haveNumbers = numberTokens[1].ReadNumbers();

				Card card = new();
				card.WinningNumbers = winningNumbers;
				card.HaveNumbers = haveNumbers;

				cards.Add(card);
			}

			return cards;
		}

		protected override int SolvePartOne(string[] input)
		{
			List<Card> cards = ReadCards(input);

			int total = 0;
			foreach (Card card in cards)
			{
				int points = 0;
				foreach (int num in card.HaveNumbers)
				{
					if (card.WinningNumbers.Contains(num))
					{
						if (points > 0) 
						{
							points *= 2;
						}
						else
						{
							points = 1;
						}
					}
				}

				total += points;
			}

			return total;
		}

		protected override int SolvePartTwo(string[] input)
		{
			List<Card> cards = ReadCards(input);
			List<int> cardCounts = new List<int>();
			for (int i = 0 ; i < cards.Count ; ++i)
			{
				cardCounts.Add(1);
			}

			for (int i = 0 ; i < cards.Count ; ++i)
			{
				int winCount = cards[i].HaveNumbers.Count(x => cards[i].WinningNumbers.Contains(x));
				for (int j = 0 ; j < winCount ; ++j)
				{
					if (( i + j + 1) < cardCounts.Count)
					{
						cardCounts[i + j + 1] += cardCounts[i];
					}
				}
			}

            return cardCounts.Sum();
		}
	}
}
