/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 19:07:33 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/06 20:54:34 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void push_stack(t_stack **a, t_stack **b)
{
	t_stack *node;

	if (!b || !*b || *b->next)
		return ;
	node = *b;
	*b = node->next;
	if (*b)
		(*b)->prev = NULL;
	node->next = *a;
	if (*a)
		(*a)->prev = node;
	node->prev = NULL;
	*a = node;
}

void pa(t_stack **a, t_stack **b)
{
	push_stack(a, b);
	write(1, "pa\n", 3);
}

void pb(t_stack **a, t_stack **b)
{
	push_stack(b, a);
	write(1, "pb\n", 3);
}