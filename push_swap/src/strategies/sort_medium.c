/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_medium.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/06 21:22:41 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/08 18:43:23 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

//need to edit this to fit disorder
static int	find_max_pos(t_stack *b, int *max_idx)
{
	int		i;
	int		pos;
	int		current_max;
	t_stack	*tmp;

	tmp = b;
	current_max = -1;
	pos = 0;
	i = 0;
	while (tmp)
	{
		if (tmp->index > current_max)
		{
			current_max = tmp->index;
			pos = i;
		}
		tmp = tmp->next;
		i++;
	}
	*max_idx = current_max;
	return (pos);
}

static void	move_max_to_top(t_stack **b)
{
	int	size;
	int	max_pos;
	int	max_idx;

	size = stack_size(*b);
	max_pos = find_max_pos(*b, &max_idx);
	if (max_pos <= size / 2)
	{
		while ((*b)->index != max_idx)
			rb(b);
	}
	else
	{
		while ((*b)->index != max_idx)
			rrb(b);
	}
}

void	sort_medium(t_stack **a, t_stack **b)
{
	int	i;
	int	range;

	index_stack(*a);
	i = 0;
	range = stack_size(*a) * 0.15 + 15;
	while (*a)
	{
		if ((*a)->index <= i)
		{
			pb(a, b);
			if (stack_size(*b) > 1)
				rb(b);
			i++;
		}
		else if ((*a)->index <= (i++) + range)
			pb(a, b);
		else
			ra(a);
	}
	while (*b)
	{
		move_max_to_top(b);
		pa(a, b);
	}
}
