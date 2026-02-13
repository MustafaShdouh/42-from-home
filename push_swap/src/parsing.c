/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 18:02:48 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/14 01:12:43 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	process_arg(char *arg, t_stack **stack_a)
{
	char	**tokens;
	int		j;
	long	nb;

	tokens = ft_split_whitespace(arg);
	if (!tokens)
		ft_error(stack_a, NULL);
	j = 0;
	while (tokens[j])
	{
		if (error_syntax(tokens[j]))
			ft_error(stack_a, NULL);
		nb = ft_atol(tokens[j]);
		if (nb > INT_MAX || nb < INT_MIN)
			ft_error(stack_a, NULL);
		if (error_duplicate(*stack_a, (int)nb))
			ft_error(stack_a, NULL);
		stack_add_back(stack_a, stack_new((int)nb));
		free(tokens[j]);
		j++;
	}
	free(tokens);
}

void	parse_args(int argc, char **argv, t_stack **stack_a)
{
	int	i;

	i = 0;
	while (i < argc)
	{
		process_arg(argv[i], stack_a);
		i++;
	}
}
