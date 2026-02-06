/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 19:11:46 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/06 20:54:43 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void swap_stack(t_stack **s)
{
	t_stack	*first;
	t_stack *second;

	if (!s || !*s || !(*s)->next)
		return ;
	first = *s;
	second = first->next;
	first->next = second->next;
	if (second->next)
		second->next->prev = first;
	second->prev = NULL;
	second->next = first;
	first->prev = second;
	*s = second;
}

void	sa(t_stack **a)
{
	swap_stack(a);
	write(1, "sa\n", 3);
}

void	sb(t_stack **b)
{
	swap_stack(b);
	write(1, "sb\n", 3);
}

void	ss(t_stack **a, t_stack **b)
{
	swap_stack(a);
	swap_stack(b);
	write(1, "ss\n", 3);
}