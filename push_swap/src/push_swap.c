/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 18:04:22 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/08 19:27:11 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../push_swap.h"
#include "../libft/libft.h"

static int	parse_flag(char *arg, t_strategy *mode, int *bench)
{
	if (ft_strncmp(arg, "--", 2) != 0)
		return (0);
	if (ft_strcmp(arg, "--simple") == 0)
		*mode = START_SIMPLE;
	else if (ft_strcmp(arg, "--medium") == 0)
		*mode = START_MEDIUM;
	else if (ft_strcmp(arg, "--complex") == 0)
		*mode = START_COMPLEX;
	else if (ft_strcmp(arg, "--adaptive") == 0)
		*mode = START_ADAPTIVE;
	else if (ft_strcmp(arg, "--bench") == 0)
		*bench = 1;
	else
		return (0);
	return (1);
}

static void	print_bench(t_strategy mode, float disorder, int ops)
{
	ft_putstr_fd("[bench] disorder: ", 2);
	ft_putfloat_fd(disorder * 100, 2);
	ft_putstr_fd("%%\n", 2);
	ft_putstr_fd("[bench] strategy: ", 2);
	if (mode == START_SIMPLE)
		ft_putstr_fd("Simple (Min-Max) | O(n^2)\n", 2);
	else if (mode == START_MEDIUM)
		ft_putstr_fd("Medium (Chunk Sort) | O(n * sqrt(n)\n", 2);
	else if (mode == START_COMPLEX)
		ft_putstr_fd("Complex (Radix) | O(n log n)\n", 2);
	else if (mode == START_ADAPTIVE)
	{
		if (disorder <= 0.2)
			ft_putstr_fd("Adaptive / O(n^2)\n", 2);
		else if (disorder <= 0.5)
			ft_putstr_fd("Adaptive / O(n * sqrt(n)\n", 2);
		else
			ft_putstr_fd("Adaptive / O(n log n)\n", 2);
	}
	ft_putstr_fd("[bench] Total Ops: ", 2);
	ft_putnbr_fd(ops, 2);
	ft_putstr_fd("\n", 2);
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