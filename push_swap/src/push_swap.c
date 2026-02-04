/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 18:04:22 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/04 22:29:25 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int parse_flag(char *arg, t_strategy *mode, int *bench)
{
	// parses the input to decide the mode (simple, medium, complex, adaptive or bench)
}

static void	print_bench(t_strategy mode, float disorder, int ops)
{
	//print the bench output
}

//this main is VERY incomplete
int	main(int argc, char **argv)
{
	t_stack	*stack_a;
	t_stack	*stack_b;
	t_strategy mode;
	int				bench;
	int				ops;
	int				i;
	float			disorder;
	
	stack_a = NULL;
	stack_b = NULL;
	mode = START_ADAPTIVE;
	bench = 0;
	ops = 0;
	i = 1;
	if (argc < 2)
		return (0);
	while (i < argc && parse_flag(argv[i], &mode, &bench))
		i++;
	if (!parse_args())
	if (ft_strncmp(argv[1], "--", 2) == 0)
	{
		if (!strcmp(argv[1], "--simple")) mode = MODE_SIMPLE;
		else if (!strcmp(argv[1], "--medium")) mode = MODE_MEDIUM;
		else if (!strcmp(argv[1], "--complex")) mode = MODE_COMPLEX;
		else if (!strcmp(argv[1], "--adaptive")) mode = MODE_ADAPTIVE;
		else if (!strcmp(argv[1], "--bench")) mode = MODE_BENCH;
		start_index++;
	}

	parse_args(argc, argv, &stack_a);

	//implement the sorting algo here

	free_stack(stack_a);
	free_stack(stack_b);
	return (0);
}