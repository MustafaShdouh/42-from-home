/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 18:02:48 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/08 18:53:00 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void parse_args(int argv, char **argv, t_stack **stack_a)
{
	int	i;
	
	long	nb;
	i = 0;
	while (i < argc)
	{
		if (error_syntax(argv[i]))
			ft_error(stack_a);
		nb = ft_atol(argv[i]);
		if (nb > INT_MAX || nb < INT_MIN)
			ft_error(stack_a);
		if (error_duplicate(argv[i], nb))
			ft_error(stack_a);
		stack_add_back(stack_a, stack_new((int)nb));
		i++;
	}
}