/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse_rotate.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 19:17:06 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/14 00:40:22 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void rev_rotate_stack(t_stack **s)
{
	t_stack	*tail;
	t_stack	*before_tail;

	if (!s || !*s || !(*s)->next)
		return ;
	tail = stack_last(*s);
	before_tail = tail->prev;
	before_tail->next = NULL;
	tail->prev = NULL;
	tail->next = *s;
	(*s)->prev = tail;
	*s = tail;
}

void	rra(t_stack **a)
{
	rev_rotate_stack(a);
	get_stats()->rra++;
	if (get_stats()->print_ops)
	write(1, "rra\n", 4);
}

void	rrb(t_stack **b)
{
	rev_rotate_stack(b);
	get_stats()->rrb++;
	if (get_stats()->print_ops)
	write(1, "rrb\n", 4);
}

void	rrr(t_stack **a, t_stack **b)
{
	rev_rotate_stack(a);
	rev_rotate_stack(b);
	get_stats()->rrr++;
	if (get_stats()->print_ops)
	write(1, "rrr\n", 4);
}