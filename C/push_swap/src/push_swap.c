/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 18:04:22 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/14 01:19:49 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include "libft.h"

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
	{
		*bench = 1;
		get_stats()->print_ops = 0;
	}
	else
		return (0);
	return (1);
}

static void	execute_sort(t_stack **a, t_stack **b, t_strategy mode)
{
	int	size;

	size = stack_size(*a);
	if (size == 2)
	{
		if ((*a)->content > (*a)->next->content)
			sa(a);
	}
	else if (size == 3)
		sort_three(a);
	else
	{
		if (mode == START_ADAPTIVE)
			sort_adaptive(a, b);
		else if (mode == START_SIMPLE)
			sort_simple(a, b);
		else if (mode == START_MEDIUM)
			sort_medium(a, b);
		else if (mode == START_COMPLEX)
			sort_complex(a, b);
	}
}

static void	init_vars(t_stack **a, t_stack **b, t_strategy *m, int *bench)
{
	*a = NULL;
	*b = NULL;
	*m = START_ADAPTIVE;
	*bench = 0;
	get_stats()->print_ops = 1;
}

int	main(int argc, char **argv)
{
	t_stack		*stack_a;
	t_stack		*stack_b;
	t_strategy	mode;
	int			bench;
	int			i;
	double		disorder;

	init_vars(&stack_a, &stack_b, &mode, &bench);
	i = 1;
	while (i < argc && parse_flag(argv[i], &mode, &bench))
		i++;
	if (i < argc)
		parse_args(argc - i, argv + i, &stack_a);
	else
		return (0);
	disorder = compute_disorder(stack_a);
	if (disorder > 0.0)
		execute_sort(&stack_a, &stack_b, mode);
	if (bench)
		print_bench(mode, disorder);
	free_stack(&stack_a);
	free_stack(&stack_b);
	return (0);
}
