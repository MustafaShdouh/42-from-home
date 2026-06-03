/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_simple.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/06 20:51:45 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/08 17:03:36 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_three(t_stack **a)
{
	int	max_val;

	max_val = find_max(*a);
	if ((*a)->content == max_val)
		ra(a);
	else if ((*a)->next->content == max_val)
		rra(a);
	if ((*a)->content > (*a)->next->content)
		sa(a);
}

static void	move_top(t_stack **a, int val)
{
	int		size;
	int		idx;
	t_stack	*tmp;

	size = stack_size(*a);
	idx = 0;
	tmp = *a;
	while (tmp && tmp->content != val)
	{
		tmp = tmp->next;
		idx++;
	}
	if (idx <= size / 2)
	{
		while ((*a)->content != val)
			ra(a);
	}
	else
		while ((*a)->content != val)
			rra(a);
}

void	sort_simple(t_stack **a, t_stack **b)
{
	int	min_val;

	if (stack_size(*a) == 2)
	{
		if ((*a)->content > (*a)->next->content)
			sa(a);
		return ;
	}
	while (stack_size(*a) > 3)
	{
		min_val = find_min(*a);
		move_top(a, min_val);
		pb(a, b);
	}
	sort_three(a);
	while (*b)
		pa(a, b);
}
